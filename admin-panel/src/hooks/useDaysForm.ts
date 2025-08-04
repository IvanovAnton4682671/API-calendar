import { FormSchema, PostInsertExternalCalendar, DayFields } from "../types/formSchemas"
import { useState, useCallback } from "react"

//функция для проверки наличия дней в форме
export function isFormWithDays(formSchema: FormSchema): formSchema is PostInsertExternalCalendar {
    return "days" in formSchema.fields
}

function useDaysForm(formSchema: FormSchema) {
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

    return {
        daysData,
        addDay,
        delDay,
        handleDayChange
    }
}

export default useDaysForm