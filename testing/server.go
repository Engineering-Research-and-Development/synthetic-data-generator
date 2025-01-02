package main

import (
	"github.com/gin-gonic/gin"
)

type ModelResponse struct {
	Model      string         `json:"model"`
	Parameters map[string]int `json:"parameters"`
}

type BehaviourResponse struct {
	Name      string  `json:"name"`
	Value     float64 `json:"value"`
	Threshold float64 `json:"threshold"`
}

func main() {
	router := gin.Default()

	router.GET("/model", modelHandler)
	router.GET("/behaviour", behaviourHandler)

	println("Server is running on http://localhost:8111")
	router.Run(":8111")
}

func modelHandler(c *gin.Context) {
	response := ModelResponse{
		Model: "modelname",
		Parameters: map[string]int{
			"a": 1,
			"b": 2,
		},
	}

	c.JSON(200, response)
}

func behaviourHandler(c *gin.Context) {
	response := BehaviourResponse{
		Name:      "avg",
		Value:     50,
		Threshold: 1.2,
	}
	c.JSON(200, response)
}
