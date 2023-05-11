import numpy as np

from keras_core import backend
from keras_core import layers
from keras_core import testing


class DicretizationTest(testing.TestCase):
    def test_discretization_basics(self):
        self.run_layer_test(
            layers.Discretization,
            init_kwargs={
                "bin_boundaries": [0.0, 0.5, 1.0],
            },
            input_shape=(2, 3),
            expected_output_shape=(2, 3),
            expected_num_trainable_weights=0,
            expected_num_non_trainable_weights=0,
            expected_num_seed_generators=0,
            expected_num_losses=0,
            supports_masking=False,
        )

    def test_adapt_flow(self):
        layer = layers.Discretization(num_bins=4)
        layer.adapt(
            np.random.random((32, 3)),
            batch_size=8,
        )
        output = layer(np.array([[0.0, 0.1, 0.3]]))
        self.assertTrue(output.dtype, "int32")

    def test_correctness(self):
        layer = layers.Discretization(bin_boundaries=[0.0, 0.5, 1.0])
        output = layer(np.array([[0.0, 0.1, 0.8]]))
        self.assertTrue(backend.is_tensor(output))
        self.assertAllClose(output, np.array([[1, 1, 2]]))