# AUTO-GENERATED FROM TypeScript
# Mock Zod
# CONVERSION STAGE: STAGE 3

class ZodString:
    def __init__(self):
        self.checks = []
    
    def min(self, length, message=None):
        self.checks.append(lambda x: len(x) >= length)
        return self
        
    def email(self, message=None):
        self.checks.append(lambda x: '@' in x) # basic check
        return self

class ZodObject:
    def __init__(self, shape):
        self.shape = shape

class Zod:
    @staticmethod
    def object(shape):
        return ZodObject(shape)
        
    @staticmethod
    def string():
        return ZodString()

    # infer type helper
    @staticmethod
    def infer(schema):
        return dict

z = Zod()
