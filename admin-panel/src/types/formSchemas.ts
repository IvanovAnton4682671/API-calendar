interface FieldBase { //база для различных полей
    label: string
    required: boolean
}

interface TextField extends FieldBase { //текстовое поле
    type: "text"
    placeholder: string
    hint: string
}

interface NumberField extends FieldBase { //числовое поле
    type: "number"
    placeholder: string
    hint: string
}

interface SwitchField extends FieldBase { //switch-переключатель
    type: "switch"
    default: boolean
}

interface RadioField extends FieldBase { //радио-кнопки
    type: "radio"
    options: Record<string, string>
}

interface TextAreaField extends FieldBase {
    type: "textArea"
    placeholder: string
    hint: string
}

interface BaseSchema { //база для различных запросов
    title: string
    description: string
}

interface GetDaysByPeriod extends BaseSchema { //получение дней по периоду
    fields: {
        period: TextField
        compact: SwitchField
        weekType: RadioField
        statistic: SwitchField
    }
}

interface GetExternalCalendar extends BaseSchema { //получение календаря за год
    fields: {
        year: NumberField
        weekType: RadioField
        statistic: SwitchField
    }
}

interface PostCreateDay extends BaseSchema { //создание дня
    fields: {
        authentication: TextField
        date: TextField
        typeId: RadioField
        note: TextField
    }
}

export interface DayFields { //поля дня для импорта календаря
    date: TextField
    typeId: RadioField
    typeText: RadioField
    note?: TextField
    weekDay: RadioField
}

export interface PostInsertExternalCalendar extends BaseSchema { //импорт календаря
    fields: {
        authentication: TextField
        dateStart: TextField
        dateEnd: TextField
        workWeekType: RadioField
        period: TextField
        calendarDays?: NumberField
        calendarDaysWithoutHolidays?: NumberField
        workDays?: NumberField
        weekends?: NumberField
        holidays?: NumberField
        days: DayFields[]
    }
}

interface PutUpdateDay extends BaseSchema { //изменение дня
    fields: {
        authentication: TextField
        oldDate: TextField
        newDate: TextField
        typeId: RadioField
        note: TextField
    }
}

interface DeleteDay extends BaseSchema { //удаление дня
    fields: {
        authentication: TextField
        date: TextField
    }
}

export interface UsingJSON extends BaseSchema {
    fields: {
        jsonArea: TextAreaField
    }
}

export type FormSchema = GetDaysByPeriod | GetExternalCalendar | PostCreateDay | PostInsertExternalCalendar | PutUpdateDay | DeleteDay | UsingJSON

export type SubmitFunction = (data: any) => Promise<any>