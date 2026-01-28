#!/usr/bin/env python3
"""
Multi-Language Support for Iris Recognition System
Provides internationalization (i18n) capabilities
"""

import json
import os
from typing import Dict, Any

class LanguageManager:
    """Manages application languages and translations"""
    
    def __init__(self):
        self.current_language = "en"
        self.languages_file = "languages.json"
        self.user_preferences_file = "user_preferences.json"
        self.translations = self._load_default_translations()
        self.load_user_language_preference()
    
    def _load_default_translations(self) -> Dict[str, Dict[str, str]]:
        """Load default translations for supported languages"""
        return {
            "en": {
                "app_title": "👁️ Iris Recognition System - Advanced Biometric Platform",
                "upload_dataset": "📁 UPLOAD DATASET",
                "train_model": "🧠 TRAIN MODEL",

                "test_recognition": "🔍 TEST RECOGNITION",
                "live_recognition": "📹 LIVE RECOGNITION",
                "iris_gallery": "🖼️ IRIS GALLERY",
                "system_status": "⚙️ SYSTEM STATUS",
                "exit_system": "❌ EXIT SYSTEM",
                "settings": "⚙️ SETTINGS",
                "themes": "🎨 THEMES",
                "languages": "🌐 LANGUAGES",
                
                # Tooltips
                "tooltip_upload": "Load iris training dataset",
                "tooltip_train": "Generate or load CNN model",
                "tooltip_analytics": "Show comprehensive analytics",
                "tooltip_test": "Test iris recognition",
                "tooltip_live": "Start live video recognition",
                "tooltip_gallery": "View captured iris images",
                "tooltip_status": "View system performance",
                "tooltip_exit": "Close application",
                
                # Welcome messages
                "welcome_title": "🎯 WELCOME TO ADVANCED IRIS RECOGNITION",
                "welcome_subtitle": "Professional Biometric Authentication System",
                "system_ready": "✅ System initialized and ready",
                "enhanced_features": "🚀 ENHANCED FEATURES AVAILABLE:",
                "quick_start": "🎮 QUICK START GUIDE:",
                
                # Status messages
                "loading": "Loading...",
                "processing": "Processing...",
                "completed": "Completed",
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "info": "Information",
                
                # Gallery
                "gallery_title": "Iris Gallery",
                "gallery_auto_refresh": "Auto-Refreshing",
                "gallery_live": "LIVE",
                "gallery_last_updated": "Last updated",
                "gallery_refresh": "🔄 Refresh",
                "gallery_open_folder": "📂 Open Folder",
                "gallery_close": "❌ Close",
                "gallery_no_images": "No captured images found",
                "gallery_new_images": "new iris image(s) detected! Refreshing gallery...",
                
                # Live Recognition
                "live_starting": "Starting live recognition...",
                "live_camera_error": "Could not open camera",
                "live_instructions": "Look directly at the camera",
                "live_press_q": "Press 'q' to quit",
                "live_press_s": "Press 's' for screenshot",
                "live_confidence": "Confidence",
                "live_person": "Person",
                
                # Settings
                "settings_title": "System Settings",
                "settings_theme": "Theme Selection",
                "settings_language": "Language Selection",
                "settings_apply": "Apply Changes",
                "settings_reset": "Reset to Default",
                "settings_save": "Save Settings",
                "settings_cancel": "Cancel",
                
                # Voice Commands
                "voice_welcome": "Voice commands activated. Say 'help' for available commands.",
                "voice_goodbye": "Voice commands deactivated.",
                "voice_unknown": "Unknown command. Say 'help' for available commands.",
                "voice_error": "Sorry, there was an error executing that command.",
                "voice_start_recognition": "Starting iris recognition...",
                "voice_take_photo": "Taking photo...",
                "voice_show_gallery": "Opening iris gallery...",
                "voice_stop_recognition": "Stopping recognition...",
                "voice_help": "Available voice commands: Start recognition, Take photo, Show gallery, Stop recognition, Help",

                # Common
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "cancel": "Cancel",
                "apply": "Apply",
                "close": "Close",
                "save": "Save",
                "load": "Load",
                "delete": "Delete",
                "edit": "Edit",
                "view": "View",
                "help": "Help",
                "about": "About"
            },
            
            "es": {
                "app_title": "👁️ Sistema de Reconocimiento de Iris - Plataforma Biométrica Avanzada",
                "upload_dataset": "📁 CARGAR DATASET",
                "train_model": "🧠 ENTRENAR MODELO",
                "view_analytics": "📊 VER ANALÍTICAS",
                "test_recognition": "🔍 PROBAR RECONOCIMIENTO",
                "live_recognition": "📹 RECONOCIMIENTO EN VIVO",
                "iris_gallery": "🖼️ GALERÍA DE IRIS",
                "system_status": "⚙️ ESTADO DEL SISTEMA",
                "exit_system": "❌ SALIR DEL SISTEMA",
                "settings": "⚙️ CONFIGURACIÓN",
                "themes": "🎨 TEMAS",
                "languages": "🌐 IDIOMAS",
                
                # Tooltips
                "tooltip_upload": "Cargar dataset de entrenamiento de iris",
                "tooltip_train": "Generar o cargar modelo CNN",
                "tooltip_analytics": "Mostrar analíticas completas",
                "tooltip_test": "Probar reconocimiento de iris",
                "tooltip_live": "Iniciar reconocimiento de video en vivo",
                "tooltip_gallery": "Ver imágenes de iris capturadas",
                "tooltip_status": "Ver rendimiento del sistema",
                "tooltip_exit": "Cerrar aplicación",
                
                # Welcome messages
                "welcome_title": "🎯 BIENVENIDO AL RECONOCIMIENTO AVANZADO DE IRIS",
                "welcome_subtitle": "Sistema Profesional de Autenticación Biométrica",
                "system_ready": "✅ Sistema inicializado y listo",
                "enhanced_features": "🚀 CARACTERÍSTICAS MEJORADAS DISPONIBLES:",
                "quick_start": "🎮 GUÍA DE INICIO RÁPIDO:",
                
                # Status messages
                "loading": "Cargando...",
                "processing": "Procesando...",
                "completed": "Completado",
                "error": "Error",
                "success": "Éxito",
                "warning": "Advertencia",
                "info": "Información",
                
                # Gallery
                "gallery_title": "Galería de Iris",
                "gallery_auto_refresh": "Auto-Actualización",
                "gallery_live": "EN VIVO",
                "gallery_last_updated": "Última actualización",
                "gallery_refresh": "🔄 Actualizar",
                "gallery_open_folder": "📂 Abrir Carpeta",
                "gallery_close": "❌ Cerrar",
                "gallery_no_images": "No se encontraron imágenes capturadas",
                "gallery_new_images": "nueva(s) imagen(es) de iris detectada(s)! Actualizando galería...",
                
                # Live Recognition
                "live_starting": "Iniciando reconocimiento en vivo...",
                "live_camera_error": "No se pudo abrir la cámara",
                "live_instructions": "Mire directamente a la cámara",
                "live_press_q": "Presione 'q' para salir",
                "live_press_s": "Presione 's' para captura de pantalla",
                "live_confidence": "Confianza",
                "live_person": "Persona",
                
                # Settings
                "settings_title": "Configuración del Sistema",
                "settings_theme": "Selección de Tema",
                "settings_language": "Selección de Idioma",
                "settings_apply": "Aplicar Cambios",
                "settings_reset": "Restablecer por Defecto",
                "settings_save": "Guardar Configuración",
                "settings_cancel": "Cancelar",
                
                # Common
                "yes": "Sí",
                "no": "No",
                "ok": "OK",
                "cancel": "Cancelar",
                "apply": "Aplicar",
                "close": "Cerrar",
                "save": "Guardar",
                "load": "Cargar",
                "delete": "Eliminar",
                "edit": "Editar",
                "view": "Ver",
                "help": "Ayuda",
                "about": "Acerca de"
            },
            
            "fr": {
                "app_title": "👁️ Système de Reconnaissance d'Iris - Plateforme Biométrique Avancée",
                "upload_dataset": "📁 CHARGER DATASET",
                "train_model": "🧠 ENTRAÎNER MODÈLE",
                "view_analytics": "📊 VOIR ANALYTIQUES",
                "test_recognition": "🔍 TESTER RECONNAISSANCE",
                "live_recognition": "📹 RECONNAISSANCE EN DIRECT",
                "iris_gallery": "🖼️ GALERIE D'IRIS",
                "system_status": "⚙️ ÉTAT DU SYSTÈME",
                "exit_system": "❌ QUITTER SYSTÈME",
                "settings": "⚙️ PARAMÈTRES",
                "themes": "🎨 THÈMES",
                "languages": "🌐 LANGUES",
                
                # Tooltips
                "tooltip_upload": "Charger le dataset d'entraînement d'iris",
                "tooltip_train": "Générer ou charger le modèle CNN",
                "tooltip_analytics": "Afficher les analytiques complètes",
                "tooltip_test": "Tester la reconnaissance d'iris",
                "tooltip_live": "Démarrer la reconnaissance vidéo en direct",
                "tooltip_gallery": "Voir les images d'iris capturées",
                "tooltip_status": "Voir les performances du système",
                "tooltip_exit": "Fermer l'application",
                
                # Welcome messages
                "welcome_title": "🎯 BIENVENUE DANS LA RECONNAISSANCE AVANCÉE D'IRIS",
                "welcome_subtitle": "Système Professionnel d'Authentification Biométrique",
                "system_ready": "✅ Système initialisé et prêt",
                "enhanced_features": "🚀 FONCTIONNALITÉS AMÉLIORÉES DISPONIBLES:",
                "quick_start": "🎮 GUIDE DE DÉMARRAGE RAPIDE:",
                
                # Status messages
                "loading": "Chargement...",
                "processing": "Traitement...",
                "completed": "Terminé",
                "error": "Erreur",
                "success": "Succès",
                "warning": "Avertissement",
                "info": "Information",
                
                # Gallery
                "gallery_title": "Galerie d'Iris",
                "gallery_auto_refresh": "Auto-Actualisation",
                "gallery_live": "EN DIRECT",
                "gallery_last_updated": "Dernière mise à jour",
                "gallery_refresh": "🔄 Actualiser",
                "gallery_open_folder": "📂 Ouvrir Dossier",
                "gallery_close": "❌ Fermer",
                "gallery_no_images": "Aucune image capturée trouvée",
                "gallery_new_images": "nouvelle(s) image(s) d'iris détectée(s)! Actualisation de la galerie...",
                
                # Live Recognition
                "live_starting": "Démarrage de la reconnaissance en direct...",
                "live_camera_error": "Impossible d'ouvrir la caméra",
                "live_instructions": "Regardez directement la caméra",
                "live_press_q": "Appuyez sur 'q' pour quitter",
                "live_press_s": "Appuyez sur 's' pour capture d'écran",
                "live_confidence": "Confiance",
                "live_person": "Personne",
                
                # Settings
                "settings_title": "Paramètres du Système",
                "settings_theme": "Sélection de Thème",
                "settings_language": "Sélection de Langue",
                "settings_apply": "Appliquer les Changements",
                "settings_reset": "Réinitialiser par Défaut",
                "settings_save": "Sauvegarder Paramètres",
                "settings_cancel": "Annuler",
                
                # Common
                "yes": "Oui",
                "no": "Non",
                "ok": "OK",
                "cancel": "Annuler",
                "apply": "Appliquer",
                "close": "Fermer",
                "save": "Sauvegarder",
                "load": "Charger",
                "delete": "Supprimer",
                "edit": "Modifier",
                "view": "Voir",
                "help": "Aide",
                "about": "À propos"
            }
        }
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for the current language"""
        if default is None:
            default = key
        
        return self.translations.get(self.current_language, {}).get(key, default)
    
    def set_language(self, language_code: str) -> bool:
        """Set the current language"""
        if language_code in self.translations:
            self.current_language = language_code
            self.save_user_language_preference()
            return True
        return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get list of available languages"""
        language_names = {
            "en": "English",
            "es": "Español",
            "fr": "Français"
        }
        return {code: language_names.get(code, code) for code in self.translations.keys()}
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def save_user_language_preference(self):
        """Save user language preference"""
        try:
            preferences = {}
            if os.path.exists(self.user_preferences_file):
                with open(self.user_preferences_file, 'r') as f:
                    preferences = json.load(f)
            
            preferences["language"] = self.current_language
            
            with open(self.user_preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except Exception as e:
            print(f"Error saving language preference: {e}")
    
    def load_user_language_preference(self):
        """Load user language preference"""
        try:
            if os.path.exists(self.user_preferences_file):
                with open(self.user_preferences_file, 'r') as f:
                    preferences = json.load(f)
                    self.current_language = preferences.get("language", "en")
        except Exception as e:
            print(f"Error loading language preference: {e}")
            self.current_language = "en"

# Global language manager instance
language_manager = LanguageManager()

def get_text(key: str, default: str = None) -> str:
    """Convenience function to get translated text"""
    return language_manager.get_text(key, default)

def set_language(language_code: str) -> bool:
    """Convenience function to set language"""
    return language_manager.set_language(language_code)

def get_available_languages() -> Dict[str, str]:
    """Convenience function to get available languages"""
    return language_manager.get_available_languages()

def get_current_language() -> str:
    """Convenience function to get current language"""
    return language_manager.get_current_language()
