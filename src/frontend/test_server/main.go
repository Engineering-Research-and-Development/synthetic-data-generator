package main

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

var db = make(map[string]interface{}) // Temporary in-memory NoSQL database

func main() {
	// Initialize Gin router
	r := gin.Default()

	// Enable CORS for all origins
	r.Use(cors.Default())

	// Load JSON data into the in-memory database
	loadData()

	// Define the /models endpoint
	r.GET("/models", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"built_in":       db["built_in"],
			"trained_models": db["trained_models"],
		})
	})

	// Start the server
	r.Run(":8090")
}

// Load JSON data into the in-memory database
func loadData() {
	db["built_in"] = []map[string]interface{}{
		{
			"name":             "Diffusion Models",
			"description":      "A default description",
			"loss_function":    "A loss function",
			"allowed_datatype": []string{"string", "string"},
			"is_categorical":   []bool{true, true},
		},
		{
			"name":             "Variational Autoencoders (VAEs)",
			"description":      "A default description",
			"loss_function":    "A loss function",
			"allowed_datatype": []string{"string"},
			"is_categorical":   []bool{true},
		},
		{
			"name":             "Multilayer Perceptron (MLP)",
			"description":      "A default description",
			"loss_function":    "A loss function",
			"allowed_datatype": []string{"string"},
			"is_categorical":   []bool{true},
		},
		{
			"name":             "Convolutional Neural Networks (CNN)",
			"description":      "A default description",
			"loss_function":    "A loss function",
			"allowed_datatype": []string{"string"},
			"is_categorical":   []bool{true},
		},
		{
			"name":             "Recurrent Neural Networks (RNN)",
			"description":      "A default description",
			"loss_function":    "A loss function",
			"allowed_datatype": []string{"string", "string"},
			"is_categorical":   []bool{true, true},
		},
	}

	db["trained_models"] = []map[string]interface{}{
		{
			"name":           "model7",
			"id":             1,
			"dataset_name":   "A dataset",
			"input_shape":    "(9x5x1x2)",
			"algorithm_name": "T-VAEs",
			"size":           "18B",
			"version_ids":    []int{1},
		},
		{
			"name":           "model4",
			"id":             2,
			"dataset_name":   "A dataset",
			"input_shape":    "(7x8x7x2)",
			"algorithm_name": "Multilayer Perceptron (MLP)",
			"size":           "18B",
			"version_ids":    []int{2},
		},
		{
			"name":           "model8",
			"id":             3,
			"dataset_name":   "A dataset",
			"input_shape":    "(7x9x4x3)",
			"algorithm_name": "Generative Adversarial Networks (GAN)",
			"size":           "18B",
			"version_ids":    []int{3, 9, 10, 11, 12},
		},
		{
			"name":           "model5",
			"id":             4,
			"dataset_name":   "A dataset",
			"input_shape":    "(7x1x8x1)",
			"algorithm_name": "Generative Adversarial Networks (GAN)",
			"size":           "18B",
			"version_ids":    []int{4},
		},
		{
			"name":           "model2",
			"id":             5,
			"dataset_name":   "A dataset",
			"input_shape":    "(1x1x5x4)",
			"algorithm_name": "Transformers",
			"size":           "18B",
			"version_ids":    []int{5},
		},
		{
			"name":           "model6",
			"id":             6,
			"dataset_name":   "A dataset",
			"input_shape":    "(3x8x3x5)",
			"algorithm_name": "Convolutional Neural Networks (CNN)",
			"size":           "18B",
			"version_ids":    []int{6},
		},
		{
			"name":           "model3",
			"id":             7,
			"dataset_name":   "A dataset",
			"input_shape":    "(7x9x8x2)",
			"algorithm_name": "T-VAEs",
			"size":           "18B",
			"version_ids":    []int{7, 13, 14, 15, 16},
		},
		{
			"name":           "model1",
			"id":             8,
			"dataset_name":   "A dataset",
			"input_shape":    "(4x9x5x6)",
			"algorithm_name": "Generative Adversarial Networks (GAN)",
			"size":           "18B",
			"version_ids":    []int{8},
		},
	}
}
