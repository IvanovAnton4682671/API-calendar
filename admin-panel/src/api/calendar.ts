export const testSubmit = async (formData: any) => {
    console.log(formData)
    return {
        message: "Данные успешно получены!",
        receivedData: formData,
        timestamp: new Date().toISOString()
    }
}