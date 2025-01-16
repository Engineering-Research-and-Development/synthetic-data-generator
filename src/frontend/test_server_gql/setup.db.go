package main

import (
	"github.com/glebarez/sqlite"
	"gorm.io/gorm"
	"gqlServer/graph/model"
	"log"
)

func initDB() *gorm.DB {
	// Connect to SQLite
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to connect database: %v", err)
	}

	// Auto-migrate the schema
	err = db.AutoMigrate(&model.Behaviour{}, &model.FunctionParameter{})
	if err != nil {
		log.Fatalf("failed to migrate database: %v", err)
	}

	seedDatabase(db)
	return db
}

func seedDatabase(db *gorm.DB) {
	// Check if already seeded
	var count int64
	db.Model(&model.Behaviour{}).Count(&count)
	if count > 0 {
		return
	}

	// Seed example data
	exampleBehaviours := []model.Behaviour{
		{
			Name:              "SampleBehaviour1",
			Description:       "This is the first sample behaviour.",
			FunctionReference: "function1",
			FunctionParameters: []*model.FunctionParameter{
				{Name: "param1", Type: "string"},
				{Name: "param2", Type: "int"},
			},
		},
		{
			Name:              "SampleBehaviour2",
			Description:       "This is the second sample behaviour.",
			FunctionReference: "function2",
			FunctionParameters: []*model.FunctionParameter{
				{Name: "paramA", Type: "float"},
				{Name: "paramB", Type: "boolean"},
			},
		},
	}

	for _, behaviour := range exampleBehaviours {
		db.Create(&behaviour)
	}
}
