import { FormSchema, PostInsertExternalCalendar, DayFields } from "../types/formSchemas"
import { useState, useCallback } from "react"
import { Flex, Text, Box, Button, ScrollArea, Separator, Callout } from "@radix-ui/themes"
import { QuestionMarkCircledIcon } from "@radix-ui/react-icons"
import MyTextField from "./MyFormFields/MyTextField"
import MyNumberField from "./MyFormFields/MyNumberField"
import MySwitchField from "./MyFormFields/MySwitchField"
import MyRadioField from "./MyFormFields/MyRadioField"
import MyTextAreaField from "./MyFormFields/MyTextAreaField"
import MyDialog from "./MyDialog"
import { UsingJSONSchema } from "../consts/myRequests"
import { testSubmit } from "../api/calendar"

//функция для проверки наличия дней в форме
function isFormWithDays(formSchema: FormSchema): formSchema is PostInsertExternalCalendar {
    return "days" in formSchema.fields
}

type JsonFieldState = {
    rawValue: string
    parsedValue: any
    error: string | null
}

function MyForm({ formSchema, submitFunc, onSubmitSuccess }:
    { formSchema: FormSchema, submitFunc: (data: any) => Promise<any>, onSubmitSuccess: (data: any) => void }) {
    //состояние для основной формы
    const [formData, setFormData] = useState<Record<string, any>>(() => {
        const initialState: Record<string, any> = {}
        Object.entries(formSchema.fields).forEach(([key, field]) => {
            if (key !== "days") {
                if (field.type === "switch") {
                    initialState[key] = field.default || false
                } else if (field.type === "radio") {
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

    //состояние для json-формы
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

    //обработчик изменения text area
    const handleTextAreaChange = (fieldName: string, value: any) => {
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

    //рендер обычных полей формы
    const renderBaseField = (fieldName: string, field: any) => {
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
                        onChange={(e) => handleTextAreaChange(fieldName, e.target.value)}
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

    //инициализация формата хранения данных дней
    const initializeDayData = (daySchema: DayFields) => {
        const dayData: Record<string, any> = {}
        Object.entries(daySchema).forEach(([fieldName, field]) => {
            dayData[fieldName] = field.type === "radio" ? Object.keys(field.options)[0] || "" : ""
        })
        return dayData
    }

    //состояние для массива дней
    const [daysData, setDaysData] = useState<any[]>(() => {
        if (!isFormWithDays(formSchema)) {
            return []
        }
        return formSchema.fields.days.length > 0 ?
        formSchema.fields.days.map(day => initializeDayData(day)) :
        [initializeDayData(formSchema.fields.days[0])]
    })

    //добавление дня в форму
    const addDay = useCallback(() => {
        if (!isFormWithDays(formSchema)) {
            return
        }
        setDaysData(prev => [...prev, initializeDayData(formSchema.fields.days[0])])
    }, [formSchema])

    //удаления дня из формы
    const delDay = useCallback((index: number) => {
        setDaysData(prev => {
            if (prev.length <= 1) {
                return prev
            }
            const newDays = [...prev]
            newDays.splice(index, 1)
            return newDays
        })
    }, [])

    //обработчик изменений полей дня
    const handleDayChange = useCallback((dayIndex: number, fieldName: string, value: any) => {
        setDaysData(prev => {
            if (dayIndex < 0 || dayIndex >= prev.length) {
                return prev
            }
            return prev.map((day, index) => index === dayIndex ? {...day, [fieldName]: value} : day)
        })
    }, [])

    //рендер полей дней в форме календаря
    const renderDayFields = (dayIndex: number) => {
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
                                        dataReceiver={daysData[dayIndex][fieldName] || ""}
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
                                        dataReceiver={daysData[dayIndex][fieldName] || ""}
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
                                        dataReceiver={daysData[dayIndex][fieldName] || Object.keys(field.options)[0] || ""}
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
        }
    }

    return(
        <form onSubmit={handleSubmit}>
            <Flex direction="column" gap="5">
                <ScrollArea type="auto" scrollbars="vertical" style={{maxHeight: "500px"}}>
                    <Flex direction="column" gap="5" style={{paddingRight: isFormWithDays(formSchema) ? "25px" : "0px"}}>
                        {Object.entries(formSchema.fields).map(([fieldName, field]) => {
                            if (fieldName !== "days") {
                                return renderBaseField(fieldName, field)
                            }
                            return null
                        })}
                        {"days" in formSchema.fields && formSchema.fields.days && (
                            <Box>
                                <Text as="div" size="3" mb="2" weight="bold">Дни календаря</Text>
                                <Flex direction="column" gap="3">
                                    {daysData.map((_, index) => renderDayFields(index))}
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
                    <Button type="submit" variant="soft" size="3" color="mint" style={"days" in formSchema.fields ? {width: "60%"} : {width: "100%"}}>Выполнить</Button>
                </Flex>
            </Flex>
        </form>
    )
}

export default MyForm