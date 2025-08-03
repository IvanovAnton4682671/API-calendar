import { FormSchema, SubmitFunction } from "../types/formSchemas"
import { Dialog, Flex } from "@radix-ui/themes"
import MyForm from "./MyForm"
import MyServerZone from "./MyServerZone"
import { useState } from "react"

function MyDialog({triggerButton, formSchema, submitFunc}:
    {triggerButton: React.ReactNode, formSchema: FormSchema, submitFunc: SubmitFunction}) {
    //состояние ответа сервера
    const [serverAnswer, setServerAnswer] = useState<any>(null)

    //обработчик получения ответа сервера
    const handleSubmitSuccess = (response: any) => {
        setServerAnswer(response)
    }

    //состояние сброса ответа сервера при открытии формы
    const [isOpen, setIsOpen] = useState<boolean>(false)

    //обработчик сброса ответа сервера при открытии формы
    const handleOpenChange = (open: boolean) => {
        setIsOpen(open)
        if (open) {
            setServerAnswer(null)
        }
    }

    return(
        <Dialog.Root open={isOpen} onOpenChange={handleOpenChange}>
            <Dialog.Trigger>{triggerButton}</Dialog.Trigger>
            <Dialog.Content maxWidth={serverAnswer ? "1200px" : "600px"}>
                <Flex direction="row" gap="5">
                    <Flex direction="column" width={serverAnswer ? "50%" : "100%"}>
                        <Dialog.Title size="5" mb="3">{formSchema.title}</Dialog.Title>
                        <Dialog.Description size="3" mb="5">{formSchema.description}</Dialog.Description>
                        <MyForm formSchema={formSchema} submitFunc={submitFunc} onSubmitSuccess={handleSubmitSuccess} />
                    </Flex>
                    {serverAnswer && (
                        <MyServerZone serverAnswer={serverAnswer} />
                    )}
                </Flex>
            </Dialog.Content>
        </Dialog.Root>
    )
}

export default MyDialog