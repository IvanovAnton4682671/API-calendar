import { Flex, Separator, Dialog, ScrollArea, Callout } from "@radix-ui/themes"
import { AxiosError } from "axios"

//тип для отображения ответа сервера
export type ServerResponse = {
    data?: any
    error?: AxiosError | any
}

function MyServerZone({serverResponse}: {serverResponse: ServerResponse}) {
    //форматирование ответа сервера
    const formatData = (data: any) => {
        if (typeof data === "string") {
            return data
        }
        if (data?.receivedData) {
            return `message: ${data.message}\n` +
                `receivedData:\n${JSON.stringify(data.receivedData, null, 2)}\n` +
                `timestamp: ${data.timestamp}`
        }
        return JSON.stringify(data, null, 2)
    }

    //форматирование ошибки сервера
    const formatError = (error: AxiosError | any) => {
        if (error.response) {
            const { status, statusText, data } = error.response
            return `Ошибка ${status}: ${statusText}\n\n${JSON.stringify(data, null, 2)}`
        } else if (error.request) {
            return `Сервер не ответил: ${error.message}\nURL: ${error.config.url}`
        } else {
            return `Ошибка запроса: ${error.message}`
        }
    }

    //определяем тип ответа
    const isError = !!serverResponse.error
    const content = isError ? formatError(serverResponse.error) : formatData(serverResponse.data)

    return(
        <Flex direction="row" gap="5" width="50%">
            <Separator orientation="vertical" size="4"/>
            <Flex direction="column">
                <Dialog.Title size="5" mb="3">
                    {isError ? "Ошибка сервера" : "Ответ сервера"}
                </Dialog.Title>
                <Dialog.Description size="3" mb="5">
                    {isError ? "Сервер вернул ошибку при обработке запроса" : "Успешный ответ сервера"}
                </Dialog.Description>
                <Flex direction="column" gap="5">
                    <ScrollArea type="auto" scrollbars="vertical" style={{maxHeight: "500px"}}>
                        <Callout.Root size="3" color={isError ? "red" : "mint"} style={{marginRight: "25px", width: "500px"}}>
                            <Callout.Text style={{whiteSpace: "pre-line"}}>
                                {content}
                            </Callout.Text>
                        </Callout.Root>
                    </ScrollArea>
                </Flex>
            </Flex>
        </Flex>
    )
}

export default MyServerZone