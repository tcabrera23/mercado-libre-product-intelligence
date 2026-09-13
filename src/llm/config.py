"""
Configuración de proveedores de LLM (Groq/Ollama)
Este módulo centraliza la lógica de conexión a diferentes proveedores de IA
"""

import os
from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Configuración del proveedor de LLM"""
    provider: str  # "groq" o "ollama"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "llama-3.3-70b-versatile"  # Default para Groq
    temperature: float = 0.7
    max_tokens: int = 8000


class LLMProvider:
    """Clase base para proveedores de LLM"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = None
        
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Genera una respuesta de chat"""
        raise NotImplementedError


class GroqProvider(LLMProvider):
    """Proveedor Groq"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from groq import Groq
            self.client = Groq(api_key=config.api_key)
        except ImportError:
            raise ImportError("groq no está instalado. Ejecuta: pip install groq")
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Genera una respuesta usando Groq API"""
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error en Groq API: {str(e)}")


class OllamaProvider(LLMProvider):
    """Proveedor Ollama (local)"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import requests
            self.requests = requests
            # Verificar si Ollama está disponible
            self._check_ollama_connection()
        except ImportError:
            raise ImportError("requests no está instalado")
    
    def _check_ollama_connection(self):
        """Verifica la conexión con Ollama"""
        try:
            response = self.requests.get(f"{self.config.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except Exception as e:
            raise ConnectionError(
                f"No se pudo conectar a Ollama en {self.config.base_url}. "
                f"Asegúrate de que Ollama esté ejecutándose. Error: {str(e)}"
            )
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Genera una respuesta usando Ollama API"""
        try:
            # Convertir mensajes al formato de Ollama
            prompt = self._convert_messages_to_prompt(messages)
            
            response = self.requests.post(
                f"{self.config.base_url}/api/generate",
                json={
                    "model": self.config.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.temperature,
                        "num_predict": self.config.max_tokens
                    }
                },
                timeout=120  # Timeout más largo para modelos locales
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            raise Exception(f"Error en Ollama API: {str(e)}")
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convierte mensajes en formato OpenAI a un prompt simple"""
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)


def get_llm_provider(
    provider: str = "groq",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None
) -> LLMProvider:
    """
    Factory para obtener el proveedor de LLM adecuado
    
    Args:
        provider: "groq" o "ollama"
        api_key: API key para Groq (opcional, se puede leer del .env)
        base_url: URL base para Ollama (default: http://localhost:11434)
        model: Modelo a usar (defaults según proveedor)
    
    Returns:
        LLMProvider instanciado
    
    Examples:
        # Groq
        llm = get_llm_provider("groq", api_key="tu_api_key")
        
        # Ollama local
        llm = get_llm_provider("ollama", model="llama3.2:8b")
    """
    provider = provider.lower()
    
    if provider == "groq":
        # Obtener API key del parámetro o variable de entorno
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "API key de Groq no encontrada. "
                "Proporciona api_key o configura GROQ_API_KEY en .env"
            )
        
        config = LLMConfig(
            provider="groq",
            api_key=api_key,
            model=model or "llama-3.3-70b-versatile"
        )
        return GroqProvider(config)
    
    elif provider == "ollama":
        # Configurar URL base de Ollama
        if not base_url:
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        config = LLMConfig(
            provider="ollama",
            base_url=base_url,
            model=model or "llama3.2:8b"  # Modelo más común de Ollama
        )
        return OllamaProvider(config)
    
    else:
        raise ValueError(f"Proveedor no soportado: {provider}. Usa 'groq' o 'ollama'")


def list_ollama_models(base_url: str = "http://localhost:11434") -> List[str]:
    """
    Lista los modelos disponibles en Ollama
    
    Args:
        base_url: URL base de Ollama
    
    Returns:
        Lista de nombres de modelos
    """
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        return [model.get("name") for model in models]
    except Exception as e:
        print(f"⚠️ Error al listar modelos de Ollama: {e}")
        return []


# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Testing LLM Providers\n")
    
    # Test 1: Groq (si está configurado)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        print("✅ Testing Groq...")
        try:
            llm = get_llm_provider("groq", api_key=groq_api_key)
            response = llm.chat_completion([
                {"role": "user", "content": "Di 'Hola' en una palabra"}
            ])
            print(f"   Response: {response}\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
    else:
        print("⚠️ GROQ_API_KEY no configurada, saltando test de Groq\n")
    
    # Test 2: Ollama (si está disponible)
    print("✅ Testing Ollama...")
    try:
        models = list_ollama_models()
        if models:
            print(f"   Modelos disponibles: {', '.join(models)}")
            llm = get_llm_provider("ollama", model=models[0])
            response = llm.chat_completion([
                {"role": "user", "content": "Di 'Hola' en una palabra"}
            ])
            print(f"   Response: {response}\n")
        else:
            print("   ⚠️ No hay modelos disponibles en Ollama\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("✨ Tests completados")
