import { FormSchema } from "../types/formSchemas"
import useBaseForm from "../hooks/useBaseForm"
import useDaysForm from "../hooks/useDaysForm"
import { isFormWithDays } from "../hooks/useDaysForm"
import { Flex, ScrollArea, Box, Text, Button, Callout } from "@radix-ui/themes"
import { QuestionMarkCircledIcon } from "@radix-ui/react-icons"
import BaseFieldRenderer from "./MyFormFields/BaseFieldRenderer"
import DayFieldRenderer from "./MyFormFields/DayFieldRenderer"
import MyDialog from "./MyDialog"
import { UsingJSONSchema } from "../consts/myRequests"
import { testSubmit } from "../api/calendarRequests"

function MyFormConstructor({formSchema, submitFunc, onSubmitSuccess, onSubmitError}:
    {
        formSchema: FormSchema,
        submitFunc: (data: any) => Promise<any>,
        onSubmitSuccess: (data: any) => void,
        onSubmitError: (error: any) => void
    }) {
    //состояния и методы для работы с обычной формой
    const { formData, jsonData, handleChange, handleJSONAreaChange } = useBaseForm(formSchema)

    //состояния и методы для работы с днями формы
    const { daysData, addDay, delDay, handleDayChange } = useDaysForm(formSchema)

    //обработчик отправки формы
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        e.stopPropagation()

        //проверяем ошибки в json`е
        const jsonErrors: string[] = []
        Object.entries(jsonData).forEach(([key, state]) => {
            if (state.error) {
                jsonErrors.push(`Поле ${key}: ${state.error}`)
            }
        })
        if (jsonErrors.length > 0) {
            alert(`Ошибки в JSON:\n${jsonErrors.join("\n")}`)
            return
        }

        //собираем данные формы
        const formValues: Record<string, any> = {...formData}
        Object.entries(jsonData).forEach(([key, state]) => {
            formValues[key] = state.parsedValue
        })

        //добавляем дни если есть
        if (isFormWithDays(formSchema)) {
            formValues.days = daysData.map(day => ({...day}))
        }

        //отправка запроса
        try {
            const response = await submitFunc(formValues)
            onSubmitSuccess(response)
        } catch (error: any) {
            console.error(`Ошибка при отправке данных: ${error}`)
            onSubmitError(error)
        }
    }

    return(
        <form onSubmit={handleSubmit}>
            <Flex direction="column" gap="5">
                <ScrollArea type="auto" scrollbars="vertical" style={{maxHeight: "500px"}}>
                    <Flex direction="column" gap="5" style={{paddingRight: isFormWithDays(formSchema) ? "25px" : "0px"}}>
                        {Object.entries(formSchema.fields).map(([fieldName, field]) => {
                            if (fieldName !== "days") {
                                return <BaseFieldRenderer
                                    key={fieldName}
                                    fieldName={fieldName}
                                    field={field}
                                    formData={formData}
                                    jsonData={jsonData}
                                    handleChange={handleChange}
                                    handleJSONAreaChange={handleJSONAreaChange}
                                />
                            }
                            return null
                        })}
                        {"days" in formSchema.fields && formSchema.fields.days && (
                            <Box>
                                <Text as="div" size="3" mb="2" weight="bold">Дни календаря</Text>
                                <Flex direction="column" gap="3">
                                    {daysData.map((day, index) => (
                                        <DayFieldRenderer
                                            key={index}
                                            formSchema={formSchema}
                                            dayIndex={index}
                                            delDay={delDay}
                                            dayData={day}
                                            handleDayChange={handleDayChange}
                                        />
                                    ))}
                                    <Flex align="center" gap="3">
                                        <Text as="div" size="2" mb="2" weight="bold">День {daysData.length + 1}</Text>
                                        <Button
                                            variant="soft"
                                            size="2"
                                            color="mint"
                                            style={{cursor: "pointer"}}
                                            onClick={() => addDay()}
                                            type="button"
                                        >
                                            Добавить день
                                        </Button>
                                    </Flex>
                                </Flex>
                            </Box>
                        )}
                    </Flex>
                </ScrollArea>
                <Flex gap="3" align="end">
                    {"days" in formSchema.fields && formSchema.fields.days && (
                        <Flex direction="column" gap="3" width="40%">
                            <Callout.Root size="1" color="indigo">
                                <Flex align="center" gap="3">
                                    <Callout.Icon>
                                        <QuestionMarkCircledIcon/>
                                    </Callout.Icon>
                                    <Callout.Text>Слишком много дней?</Callout.Text>
                                </Flex>
                            </Callout.Root>
                            <MyDialog
                                triggerButton={
                                    <Button type="button" variant="soft" size="3" color="orange">Использовать JSON</Button>
                                }
                                formSchema={UsingJSONSchema}
                                submitFunc={testSubmit}
                            />
                        </Flex>
                    )}
                    <Button
                        type="submit"
                        variant="soft"
                        size="3"
                        color="mint"
                        style={"days" in formSchema.fields ? {width: "60%"} : {width: "100%"}}
                    >
                        Выполнить
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

export default MyFormConstructor