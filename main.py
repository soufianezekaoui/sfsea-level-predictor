import sea_level_predictor
from unittest import main

print("="*60)
print("🧪 SEA LEVEL PREDICTOR - Test Runner")
print("="*60)

# Run unit tests if available
print("\n🧪 Running unit tests...")
print("="*60)

try:
    main(module='test_module', exit=False, verbosity=2)
except ModuleNotFoundError:
    print("\n⚠️  test_module.py not found")
    print("💡 Get it from: https://github.com/freeCodeCamp/boilerplate-sea-level-predictor")

