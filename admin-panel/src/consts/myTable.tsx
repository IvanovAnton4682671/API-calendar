import { TableRequestsSchema } from "../types/tableForms"
import { Button } from "@radix-ui/themes"
import { GetDaysByPeriodSchema,
    GetExternalCalendarSchema,
    PostCreateDaySchema,
    PostInsertExternalCalendarSchema,
    PutUpdateDaySchema,
    DeleteDaySchema } from "./myRequests"
import { testSubmit,
    getDaysByPeriod,
    getExternalCalendar,
    postCreateDay,
    postInsertExternalCalendar,
    putUpdateDay,
    deleteDay } from "../api/calendarRequests"

export const MyTable: TableRequestsSchema = {
    columns: [
        {
            title: "GET",
            color: "indigo",
            items: [
                {
                    button: <Button variant="soft" size="3" color="indigo" style={{cursor: "pointer"}}>Получить дни за период</Button>,
                    data: GetDaysByPeriodSchema,
                    submitFunc: getDaysByPeriod
                },
                {
                    button: <Button variant="soft" size="3" color="indigo" style={{cursor: "pointer"}}>Получить календарь за год</Button>,
                    data: GetExternalCalendarSchema,
                    submitFunc: getExternalCalendar
                }
            ]
        },
        {
            title: "POST",
            color: "mint",
            items: [
                {
                    button: <Button variant="soft" size="3" color="mint" style={{cursor: "pointer"}}>Создать день</Button>,
                    data: PostCreateDaySchema,
                    submitFunc: postCreateDay
                },
                {
                    button: <Button variant="soft" size="3" style={{cursor: "pointer"}}>Импортировать календарь</Button>,
                    data: PostInsertExternalCalendarSchema,
                    submitFunc: postInsertExternalCalendar
                }
            ]
        },
        {
            title: "PUT",
            color: "orange",
            items: [
                {
                    button: <Button variant="soft" size="3" color="orange" style={{cursor: "pointer"}}>Изменить день</Button>,
                    data: PutUpdateDaySchema,
                    submitFunc: putUpdateDay
                }
            ]
        },
        {
            title: "DELETE",
            color: "red",
            items: [
                {
                    button: <Button variant="soft" size="3" color="red" style={{cursor: "pointer"}}>Удалить день</Button>,
                    data: DeleteDaySchema,
                    submitFunc: deleteDay
                }
            ]
        }
    ]
}