package model

type Behaviour struct {
	ID                 int32                `gorm:"primaryKey" json:"id"`
	Name               string               `json:"name"`
	Description        string               `json:"description"`
	FunctionReference  string               `json:"function_reference"`
	FunctionParameters []*FunctionParameter `gorm:"foreignKey:BehaviourID" json:"function_parameters"`
}

type FunctionParameter struct {
	ID          int32  `gorm:"primaryKey" json:"id"`
	BehaviourID int    `json:"behaviour_id"` // Foreign key
	Name        string `json:"name"`
	Type        string `json:"type"`
}
