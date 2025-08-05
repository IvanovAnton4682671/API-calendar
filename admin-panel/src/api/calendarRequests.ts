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
            `/api/period/${formValues.period}?compact=${formValues.compact}&week_type=${formValues.weekType}&statistic=${formValues.statistic}`,
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
            `/api/external/period/${formSchema.year}?week_type=${formSchema.weekType}&statistic=${formSchema.statistic}`,
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