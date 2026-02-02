

import threading

try:
    import speech_recognition as sr
except Exception:
    sr = None

_lock = threading.Lock()
_quit_requested = False
_start_requested = False
_restart_requested = False


def request_quit():
    global _quit_requested
    with _lock:
        _quit_requested = True


def request_start():
    global _start_requested
    with _lock:
        _start_requested = True


def request_restart():
    global _restart_requested
    with _lock:
        _restart_requested = True


def should_quit() -> bool:
    with _lock:
        return _quit_requested


def consume_start() -> bool:
    global _start_requested
    with _lock:
        v = _start_requested
        _start_requested = False
        return v


def consume_restart() -> bool:
    global _restart_requested
    with _lock:
        v = _restart_requested
        _restart_requested = False
        return v


def _voice_worker(language="pt-BR"):
    if sr is None:
        return

    r = sr.Recognizer()

    try:
        mic = sr.Microphone()
    except Exception:
        return

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.8)
    except Exception:
        pass

    while True:
        if should_quit():
            return
        try:
            with mic as source:
                audio = r.listen(source, timeout=1, phrase_time_limit=2.7)

            text = r.recognize_google(audio, language=language)
            if not text:
                continue

            t = text.lower().strip()

            if "sair" in t:
                request_quit()
                return
            if "jogar" in t:
                request_start()
            if "reiniciar" in t:
                request_restart()

        except sr.WaitTimeoutError:
            continue
        except Exception:
            continue


def start_voice_listener(language="pt-BR"):
    
    if sr is None:
        return None
    t = threading.Thread(target=_voice_worker, args=(language,), daemon=True)
    t.start()
    return t
