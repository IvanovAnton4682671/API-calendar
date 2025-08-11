import { FormSchema, UsingJSON } from "../types/formSchemas";

export const GetDaysByPeriodSchema: FormSchema = {
    title: "Получить дни за период",
    description: "Позволяет получить календарные дни за определённый период с дополнительными параметрами",
    fields: {
        period: {
            type: "text",
            label: "Период",
            placeholder: "Введите временной период",
            hint: "Поддерживаемые форматы периода:\nГод: ГГГГ (Пример: 2025)\nКвартал: QNГГГГ (Пример: Q12025)\nМесяц: ММ.ГГГГ (Пример: 01.2025)\nСутки: ДД.ММ.ГГГГ (Пример: 01.01.2025)\nПроизвольный период: ДД.ММ.ГГГГ-ДД.ММ.ГГГГ (Пример: 01.01.2025-10.01.2025)",
            required: true
        },
        compact: {
            type: "switch",
            label: "Компактный формат вывода",
            default: false,
            required: false
        },
        week_type: {
            type: "radio",
            label: "Тип рабочей недели",
            options: {
                "5": "5-дневная",
                "6": "6-дневная"
            },
            required: true
        },
        statistic: {
            type: "switch",
            label: "Дополнительная статистика",
            default: false,
            required: false
        },
    }
}

export const GetExternalCalendarSchema: FormSchema = {
    title: "Получить календарь за год",
    description: "Позволяет получить производственный календарь за определённый год с дополнительными параметрами",
    fields: {
        year: {
            type: "number",
            label: "Год",
            placeholder: "Введите год",
            hint: "Поддерживаемый формат года:\nГГГГ (Пример: 2025)",
            required: true
        },
        week_type: {
            type: "radio",
            label: "Тип рабочей недели",
            options: {
                "5": "5-дневная",
                "6": "6-дневная"
            },
            required: true
        },
        statistic: {
            type: "switch",
            label: "Дополнительная статистика",
            default: false,
            required: false
        }
    }
}

export const PostCreateDaySchema: FormSchema = {
    title: "Создать день",
    description: "Позволяет создать календарный день (доступ по токену)",
    fields: {
        authentication: {
            type: "text",
            label: "Токен аутентификации",
            placeholder: "Введите секретный токен доступа",
            hint: "Поддерживаемый формат токена аутентификации (без <>):\nBearer <токен> (Пример: Bearer token)",
            required: true
        },
        date: {
            type: "text",
            label: "Дата дня",
            placeholder: "Введите дату дня",
            hint: "Поддерживаемый формат даты дня:\nГГГГ-ММ-ДД (Пример: 2025-01-01)",
            required: true
        },
        type_id: {
            type: "radio",
            label: "Тип дня",
            options: {
                "1": "1",
                "2": "2",
                "3": "3"
            },
            required: true
        },
        note: {
            type: "text",
            label: "Описание дня",
            placeholder: "Введите дополнительное описание дня",
            hint: "Опциональное описание дня",
            required: false
        }
    }
}

export const PostInsertExternalCalendarSchema: FormSchema = {
    title: "Импортировать календарь",
    description: "Позволяет импортировать производственный календарь произвольного размера (доступ по токену)",
    fields: {
        authentication: {
            type: "text",
            label: "Токен аутентификации",
            placeholder: "Введите секретный токен доступа",
            hint: "Поддерживаемый формат токена аутентификации (без <>):\nBearer <токен> (Пример: Bearer token)",
            required: true
        },
        date_start: {
            type: "text",
            label: "Дата начала периода",
            placeholder: "Введите дату начала периода",
            hint: "Поддерживаемый формат даты:\nДД.ММ.ГГГГ (Пример: 01.01.2025)",
            required: true
        },
        date_end: {
            type: "text",
            label: "Дата конца периода",
            placeholder: "Введите дату конца периода",
            hint: "Поддерживаемый формат даты:\nДД.ММ.ГГГГ (Пример: 01.01.2025)",
            required: true
        },
        work_week_type: {
            type: "radio",
            label: "Тип рабочей недели",
            options: {
                "5": "5-дневная",
                "6": "6-дневная"
            },
            required: true
        },
        period: {
            type: "select",
            label: "Временной период",
            options: {
                "Год": "Год",
                "Квартал": "Квартал",
                "Месяц": "Месяц",
                "Сутки": "Сутки",
                "Произвольный период": "Произвольный период",
            },
            required: true
        },
        days: [
            {
                date: {
                    type: "text",
                    label: "Дата дня",
                    placeholder: "Введите дату дня",
                    hint: "Поддерживаемый формат даты:\nДД.ММ.ГГГГ (Пример: 01.01.2025)",
                    required: true
                },
                type_id: {
                    type: "radio",
                    label: "Тип дня",
                    options: {
                        "1": "1",
                        "2": "2",
                        "3": "3"
                    },
                    required: true
                },
                type_text: {
                    type: "radio",
                    label: "Название типа дня",
                    options: {
                        "Рабочий день": "Рабочий день",
                        "Выходной день": "Выходной день",
                        "Государственный праздник": "Государственный праздник"
                    },
                    required: true
                },
                note: {
                    type: "text",
                    label: "Описание дня",
                    placeholder: "Введите дополнительное описание дня",
                    hint: "Опциональное описание дня",
                    required: false
                },
                week_day: {
                    type: "radio",
                    label: "День недели",
                    options: {
                        "пн": "пн",
                        "вт": "вт",
                        "ср": "ср",
                        "чт": "чт",
                        "пт": "пт",
                        "сб": "сб",
                        "вс": "вс"
                    },
                    required: true
                }
            },
        ]
    }
}

export const PutUpdateDaySchema: FormSchema = {
    title: "Изменить день",
    description: "Позволяет изменить календарный день по дате (доступ по токену)",
    fields: {
        authentication: {
            type: "text",
            label: "Токен аутентификации",
            placeholder: "Введите секретный токен доступа",
            hint: "Поддерживаемый формат токена аутентификации (без <>):\nBearer <токен> (Пример: Bearer token)",
            required: true
        },
        old_date: {
            type: "text",
            label: "Дата изменяемого дня",
            placeholder: "Введите дату изменяемого дня",
            hint: "Поддерживаемый формат даты дня:\nГГГГ-ММ-ДД (Пример: 2025-01-01)",
            required: true
        },
        new_date: {
            type: "text",
            label: "Новая дата дня",
            placeholder: "Введите новую дату дня",
            hint: "Поддерживаемый формат даты дня:\nГГГГ-ММ-ДД (Пример: 2025-01-01)",
            required: true
        },
        type_id: {
            type: "radio",
            label: "Тип дня",
            options: {
                "1": "1",
                "2": "2",
                "3": "3"
            },
            required: true
        },
        note: {
            type: "text",
            label: "Описание дня",
            placeholder: "Введите дополнительное описание дня",
            hint: "Опциональное описание дня",
            required: false
        }
    }
}

export const DeleteDaySchema: FormSchema = {
    title: "Удалить день",
    description: "Позволяет удалить календарный день по дате (доступ по токену)",
    fields: {
        authentication: {
            type: "text",
            label: "Токен аутентификации",
            placeholder: "Введите секретный токен доступа",
            hint: "Поддерживаемый формат токена аутентификации (без <>):\nBearer <токен> (Пример: Bearer token)",
            required: true
        },
        date: {
            type: "text",
            label: "Дата дня",
            placeholder: "Введите дату дня",
            hint: "Поддерживаемый формат даты дня:\nГГГГ-ММ-ДД (Пример: 2025-01-01)",
            required: true
        },
    }
}

export const UsingJSONSchema: UsingJSON = {
    title: "Использовать JSON",
    description: "Позволяет ввести данные производственного календаря в JSON-формате",
    fields: {
        jsonArea: {
            type: "textArea",
            label: "Календарь в JSON-формате",
            placeholder: "Введите данные календаря в JSON-формате",
            hint: 'Пример JSON-календаря:\n{\n"authentication": "Bearer токен",\n"date_start": "01.01.2025",\n"date_end": "02.01.2025",\n"work_week_type": 5,\n"period": "Произвольный период",\n"days": [\n{\n"date": "01.01.2025",\n"type_id": 3,\n"type_text": "Государственный праздник",\n"note": "Новогодние каникулы",\n"week_day": "ср"\n},\n...\n]\n}',
            required: true
        }
    }
}