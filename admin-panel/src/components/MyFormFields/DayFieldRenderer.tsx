import { isFormWithDays } from "../../hooks/useDaysForm"
import { FormSchema } from "../../types/formSchemas"
import { Box, Flex, Text, Button, Separator } from "@radix-ui/themes"
import MyTextField from "./MyTextField"
import MyNumberField from "./MyNumberField"
import MyRadioField from "./MyRadioField"

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
                        default:
                            return null
                    }
                })}
            </Flex>
            <Separator my="5" size="4"/>
        </Box>
    )
}

export default DayFieldRenderer