import { FormSchema } from "../types/formSchemas"
import { useState } from "react"

function useBaseForm(formSchema: FormSchema) {
    //состояние для основной формы
    const [formData, setFormData] = useState<Record<string, any>>(() => {
        const initialState: Record<string, any> = {}
        Object.entries(formSchema.fields).forEach(([key, field]) => {
            if (key !== "days") {
                if (field.type === "switch") {
                    initialState[key] = field.default || false
                } else if (field.type === "radio" || field.type === "select") {
                    initialState[key] = Object.keys(field.options)[0] || ""
                } else {
                    initialState[key] = ""
                }
            }
        })
        return initialState
    })

    //обработчик изменений полей формы
    const handleChange = (fieldName: string, value: any) => {
        setFormData(prev => ({...prev, [fieldName]: value}))
    }

    //тип для json-поля
    type JsonFieldState = {
        rawValue: string
        parsedValue: any
        error: string | null
    }

    //состояние для json-поля
    const [jsonData, setJSONData] = useState<Record<string, JsonFieldState>>(() => {
        const initialState: Record<string, JsonFieldState> = {}
        Object.entries(formSchema.fields).forEach(([key, field]) => {
            if (field.type === "textArea") {
                initialState[key] = {
                    rawValue: "",
                    parsedValue: null,
                    error: null
                }
            }
        })
        return initialState
    })

    //обработчик изменения json-поля
    const handleJSONAreaChange = (fieldName: string, value: any) => {
        setJSONData(prev => {
            const newState = {...prev}
            try {
                const parsed = JSON.parse(value)
                newState[fieldName] = {
                    rawValue: value,
                    parsedValue: parsed,
                    error: null
                }
            } catch (error: any) {
                newState[fieldName] = {
                    rawValue: value,
                    parsedValue: null,
                    error: `Ошибка JSON: ${error.message}`
                }
            }
            return newState
        })
    }

    return {
        formData,
        jsonData,
        handleChange,
        handleJSONAreaChange
    }
}

export default useBaseForm