# AUTO-GENERATED FROM TypeScript
# Mock for 'sonner' library
# CONVERSION STAGE: STAGE 3

class Toast:
    @staticmethod
    def success(message: str):
        print(f"[Toast Success] {message}")
        
    @staticmethod
    def error(message: str):
        print(f"[Toast Error] {message}")
        
    @staticmethod
    def info(message: str):
        print(f"[Toast Info] {message}")

toast = Toast()
