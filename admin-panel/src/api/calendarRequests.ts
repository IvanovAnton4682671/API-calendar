import axios from "axios"

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
        formSchema.work_week_type = String(`${Number(formSchema.work_week_type)}-дневная рабочая неделя`)
        formSchema.calendar_days = Number(formSchema.calendar_days)
        formSchema.calendar_days_without_holidays = Number(formSchema.calendar_days_without_holidays)
        formSchema.work_days = Number(formSchema.work_days)
        formSchema.weekends = Number(formSchema.weekends)
        formSchema.holidays = Number(formSchema.holidays)
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