import { isFormWithDays } from "../../hooks/useDaysForm"
import { FormSchema } from "../../types/formSchemas"
import { Box, Flex, Text, Button, Separator } from "@radix-ui/themes"
import MyTextField from "./MyTextField"
import MyNumberField from "./MyNumberField"
import MyRadioField from "./MyRadioField"
import MyDatePickerField from "./MyDatePickerField"
import React from "react"

function DayFieldRenderer({ formSchema, dayIndex, delDay, dayData, handleDayChange }:
    {
        formSchema: FormSchema,
        dayIndex: number,
        delDay: (index: number) => any,
        dayData: any,
        handleDayChange: (dayIndex: number, fieldName: string, value: any) => any
    }) {
    if (!isFormWithDays(formSchema)) {
            return null
        }
    const daySchema = formSchema.fields.days[0]
    return(
        <Box key={dayIndex}>
            <Flex align="center" gap="3">
                <Text as="div" size="2" mb="2" weight="bold">День {dayIndex + 1}</Text>
                <Button
                    variant="soft"
                    size="2"
                    color="red"
                    style={{cursor: "pointer"}}
                    onClick={() => delDay(dayIndex)}
                    type="button"
                >
                    Удалить день
                </Button>
            </Flex>
            <Flex direction="column" gap="3">
                {Object.entries(daySchema).map(([fieldName, field]) => {
                    switch (field.type) {
                        case "text":
                            return(
                                <MyTextField
                                    key={fieldName}
                                    dataReceiver={dayData[fieldName] || ""}
                                    onChange={(e) => handleDayChange(dayIndex, fieldName, e.target.value)}
                                    field={field}
                                    size="2"
                                    name={`${fieldName}-${dayIndex}`}
                                />
                            )
                        case "number":
                            return(
                                <MyNumberField
                                    key={fieldName}
                                    dataReceiver={dayData[fieldName] || ""}
                                    onChange={(e) => handleDayChange(dayIndex, fieldName, e.target.value)}
                                    field={field}
                                    size="2"
                                    name={`${fieldName}-${dayIndex}`}
                                />
                            )
                        case "radio":
                            return(
                                <MyRadioField
                                    key={fieldName}
                                    dataReceiver={dayData[fieldName] || Object.keys(field.options)[0] || ""}
                                    onValueChange={(value) => handleDayChange(dayIndex, fieldName, value)}
                                    field={field}
                                    size="2"
                                    name={`${fieldName}-${dayIndex}`}
                                />
                            )
                        case "datePicker":
                            return(
                                <MyDatePickerField
                                    key={fieldName}
                                    dataReceiver={dayData[fieldName] || ""}
                                    onChange={(value) => handleDayChange(dayIndex, fieldName, value)}
                                    field={field}
                                    size="2"
                                    name={`${fieldName}-${dayIndex}`}
                                />
                            )
                        default:
                            return null
                    }
                })}
            </Flex>
            <Separator my="5" size="4"/>
        </Box>
    )
}

//функция сравнения объектов
function shallowEqual(objA: any, objB: any) {
    if (objA === objB) return true
    if (typeof objA !== "object" || objA === null) return false

    const keysA = Object.keys(objA)
    const keysB = Object.keys(objB)
    if (keysA.length !== keysB.length) return false
    for (let i = 0; i < keysA.length; i++) {
        const key = keysA[i]
        if (objA[key] !== objB[key]) return false
    }
    return true
}

//export default DayFieldRenderer
export default React.memo(DayFieldRenderer, (prevProps, nextProps) => {
    return shallowEqual(prevProps.dayData, nextProps.dayData)
})