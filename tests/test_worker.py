import unittest

from keras import models

from worker import constructor


class TestWorker(unittest.TestCase):
    def test_constructor(self):
        layers = [
            {
                'name': 'Dense',
                'config': {
                    'units': 10
                }
            },
            {
                'name': 'Dropout',
                'config': {
                    'rate': 0.25
                }
            }
        ]
        architecture = {
            'layers': layers
        }
        shape = (10,)

        model = constructor.create_model(architecture, shape)

        self.assertEqual(type(model), models.Model)
        self.assertEqual(len(model.layers), len(layers) + 1)

    def test_consturctor_no_required(self):
        layers = [
            {
                'name': 'Dense',
                'config': {
                    'units': 10
                }
            },
            {
                'name': 'Dropout'
            }
        ]
        architecture = {
            'layers': layers
        }
        shape = (10,)

        with self.assertRaises(TypeError):
            _ = constructor.create_model(architecture, shape)

    def test_constructor_architecture_type(self):
        with self.assertRaises(TypeError):
            constructor.create_model('string', (1,))

        with self.assertRaises(TypeError):
            constructor.create_model([], (1,))

    def test_constructor_shape_type(self):
        with self.assertRaises(TypeError):
            constructor.create_model({}, 'string')

        with self.assertRaises(TypeError):
            constructor.create_model({}, 1)

        with self.assertRaises(ValueError):
            constructor.create_model({}, [])

    def test_compile(self):
        layers = [
            {
                'name': 'Dense',
                'config': {
                    'units': 10
                }
            },
            {
                'name': 'Dropout',
                'config': {
                    'rate': 0.25
                }
            }
        ]
        architecture = {
            'layers': layers
        }
        shape = (10,)

        model = constructor.create_model(architecture, shape)

        config = {
            'loss': 'mean_squared_error',
            'optimizer': {
                'name': 'SGD'
            }
        }

        constructor.compile_model(model, config)
