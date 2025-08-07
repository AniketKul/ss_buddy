import numpy as np
import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    def initialize(self, args):
        self.model_config = args['model_config']
        
    def execute(self, requests):
        responses = []
        for request in requests:
            # Get input
            input_tensor = pb_utils.get_input_tensor_by_name(request, "INPUT")
            input_data = input_tensor.as_numpy()
            
            # Create dummy output - 12 probabilities for task classification
            output_data = np.random.rand(1, 12).astype(np.float32)
            # Normalize to sum to 1 (like real probabilities)
            output_data = output_data / np.sum(output_data)
            
            # Create output tensor
            output_tensor = pb_utils.Tensor("OUTPUT", output_data)
            inference_response = pb_utils.InferenceResponse(output_tensors=[output_tensor])
            responses.append(inference_response)
            
        return responses
