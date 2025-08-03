import { ReactElement } from "react"
import { FormSchema } from "./formSchemas"

interface TableRequests { //таблица запросов к серверу
    columns: Array<{
        title: string
        color: "indigo" | "mint" | "orange" | "red"
        items: Array<{
            button: ReactElement
            data: FormSchema
            submitFunc: (data: any) => Promise<any>
        }>
    }>
}

export type TableRequestsSchema = TableRequests