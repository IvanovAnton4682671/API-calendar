import axios from "axios"
import { DayFields } from "../types/formSchemas"

export const testSubmit = async (formData: any) => {
    console.log(formData)
    return {
        message: "Данные успешно получены!",
        receivedData: formData,
        timestamp: new Date().toISOString()
    }
}

export const getDaysByPeriod = async (formValues: any) => {
    try {
        const response = await axios.get(
            `/api/period/${formValues.period}?compact=${formValues.compact}&week_type=${formValues.week_type}&statistic=${formValues.statistic}`,
            {
                headers: {
                    "Accept": "application/json"
                }
            }
        )
        return response.data
    } catch (error: any) {
        console.error("Ошибка при получении дней по периоду: ", error)
        throw error
    }
}

export const getExternalCalendar = async (formSchema: any) => {
    try {
        const response = await axios.get(
            `/api/external/period/${formSchema.year}?week_type=${formSchema.week_type}&statistic=${formSchema.statistic}`,
            {
                headers: {
                    "Accept": "application/json"
                }
            }
        )
        return response.data
    } catch (error: any) {
        console.error("Ошибка при получении календаря из внешнего источника: ", error)
        throw error
    }
}

export const postCreateDay = async (formSchema: any) => {
    try {
        formSchema.type_id = Number(formSchema.type_id)
        const response = await axios.post(
            `/api/date?note=${formSchema.note}`,
            formSchema,
            {
                headers: {
                    "Accept": "application/json",
                    "Authentication": formSchema.authentication,
                    "Content-Type": "application/json"
                }
            }
        )
        return response.data
    } catch (error: any) {
        console.error("Ошибка при создании дня: ", error)
        throw error
    }
}

export const postInsertExternalCalendar = async (formSchema: any) => {
    try {
        if (formSchema.jsonArea) {
            console.log("До форматирования: ", formSchema)
            const authToken = String(formSchema.jsonArea.authentication)
            formSchema.date_start = String(formSchema.jsonArea.date_start)
            formSchema.date_end = String(formSchema.jsonArea.date_end)
            formSchema.work_week_type = String(`${Number(formSchema.jsonArea.work_week_type)}-дневная рабочая неделя`)
            formSchema.period = String(formSchema.jsonArea.period)
            formSchema.days = formSchema.jsonArea.days
            delete formSchema.jsonArea
            console.log("После форматирования: ", formSchema)
            const response = await axios.post(
                `/api/external/insert_production_calendar`,
                formSchema,
                {
                    headers: {
                        "Accept": "application/json",
                        "Authentication": authToken,
                        "Content-Type": "application/json"
                    }
                }
            )
            return response.data
        } else {
            formSchema.work_week_type = String(`${Number(formSchema.work_week_type)}-дневная рабочая неделя`)
            console.log(formSchema)
            formSchema.days.forEach((day: any) => {
                let type_id = day.type_id
                if (type_id === "1") day.type_text = "Рабочий день"
                else if (type_id === "2") day.type_text = "Выходной день"
                else if (type_id === "3") day.type_text = "Государственный праздник"
            });
            const response = await axios.post(
                `/api/external/insert_production_calendar`,
                formSchema,
                {
                    headers: {
                        "Accept": "application/json",
                        "Authentication": formSchema.authentication,
                        "Content-Type": "application/json"
                    }
                }
            )
            return response.data
        }
    } catch (error: any) {
        console.error("Ошибка при импорте календаря: ", error)
        throw error
    }
}

export const putUpdateDay = async (formSchema: any) => {
    try {
        formSchema.date = formSchema.new_date
        const response = await axios.put(
            `/api/date/${formSchema.old_date}?note=${formSchema.note}`,
            formSchema,
            {
                headers: {
                    "Accept": "application/json",
                    "Authentication": formSchema.authentication,
                    "Content-Type": "application/json"
                }
            }
        )
        return response.data
    } catch (error: any) {
        console.error("Ошибка при изменении дня: ", error)
        throw error
    }
}

export const deleteDay = async (formSchema: any) => {
    try {
        const response = await axios.delete(
            `/api/date/${formSchema.date}`,
            {
                headers: {
                    "Accept": "application/json",
                    "Authentication": formSchema.authentication,
                    "Content-Type": "application/json"
                }
            }
        )
        return response.data
    } catch (error: any) {
        console.error("Ошибка при удалении дня: ", error)
        throw error
    }
}