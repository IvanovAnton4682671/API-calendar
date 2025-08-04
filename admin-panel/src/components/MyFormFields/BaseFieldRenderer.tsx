import MyTextField from "./MyTextField"
import MyNumberField from "./MyNumberField"
import MySwitchField from "./MySwitchField"
import MyRadioField from "./MyRadioField"
import MyTextAreaField from "./MyTextAreaField"

function BaseFieldRenderer({fieldName, field, formData, jsonData, handleChange, handleJSONAreaChange}:
    {
        fieldName: string,
        field: any,
        formData: any,
        jsonData: any,
        handleChange: (fieldName: string, value: any) => void,
        handleJSONAreaChange: (fieldName: string, value: any) => void
    }) {
    switch (field.type) {
            case "text":
                return(
                    <MyTextField
                        key={fieldName}
                        dataReceiver={formData[fieldName] || ""}
                        onChange={(e) => handleChange(fieldName, e.target.value)}
                        field={field}
                        size="3"
                        name={fieldName}
                    />
                )
            case "number":
                return(
                    <MyNumberField
                        key={fieldName}
                        dataReceiver={formData[fieldName] || ""}
                        onChange={(e) => handleChange(fieldName, e.target.value)}
                        field={field}
                        size="3"
                        name={fieldName}
                    />
                )
            case "switch":
                return(
                    <MySwitchField
                        key={fieldName}
                        dataReceiver={formData[fieldName] || ""}
                        onCheckedChange={(checked) => handleChange(fieldName, checked)}
                        field={field}
                        leftText="Нет"
                        rightText="Да"
                        size="3"
                        name={fieldName}
                    />
                )
            case "radio":
                return(
                    <MyRadioField
                        key={fieldName}
                        dataReceiver={formData[fieldName] || ""}
                        onValueChange={(value) => handleChange(fieldName, value)}
                        field={field}
                        size="3"
                        name={fieldName}
                    />
                )
            case "textArea":
                return(
                    <MyTextAreaField
                        key={fieldName}
                        dataReceiver={jsonData[fieldName].rawValue || ""}
                        onChange={(e) => handleJSONAreaChange(fieldName, e.target.value)}
                        field={field}
                        size="3"
                        areaSize="3"
                        name={fieldName}
                    />
                )
            default:
                return null
        }
}

export default BaseFieldRenderer