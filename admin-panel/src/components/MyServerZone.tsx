import { Flex, Separator, Dialog, ScrollArea, Callout } from "@radix-ui/themes"

function MyServerZone({serverAnswer}: {serverAnswer: any}) {
    //форматирование ответа сервера
    const formatAnswer = (answer: any) => {
        if (typeof answer === "string") {
            return answer
        }
        if (answer.receivedData) {
            return `message: ${answer.message}\n` +
                `receivedData:\n${JSON.stringify(answer.receivedData, null, 2)}\n` +
                `timestamp: ${answer.timestamp}`
        }
        return JSON.stringify(answer, null, 2)
    }

    return(
        <Flex direction="row" gap="5" width="50%">
            <Separator orientation="vertical" size="4"/>
            <Flex direction="column">
                <Dialog.Title size="5" mb="3">Ответ сервера</Dialog.Title>
                <Dialog.Description size="3" mb="5">Здесь располагается ответ сервера на ваш запрос</Dialog.Description>
                <Flex direction="column" gap="5">
                    <ScrollArea type="auto" scrollbars="vertical" style={{maxHeight: "500px"}}>
                        <Callout.Root size="3" color="green" style={{marginRight: "25px", width: "500px"}}>
                            <Callout.Text style={{whiteSpace: "pre-line"}}>
                                {formatAnswer(serverAnswer)}
                            </Callout.Text>
                        </Callout.Root>
                    </ScrollArea>
                </Flex>
            </Flex>
        </Flex>
    )
}

export default MyServerZone