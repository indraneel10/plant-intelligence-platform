class PlantIntelligenceError(Exception): pass
class DeviceError(PlantIntelligenceError): pass
class VisionError(PlantIntelligenceError): pass
class SafetyViolation(PlantIntelligenceError): pass
