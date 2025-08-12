export const dateParse = (date: string) => {
    const parts = date.split("-")
    if (parts.length !== 3) throw new Error("Некорректный формат даты!")
    const [year, month, day] = parts
    return `${day}.${month}.${year}`
}