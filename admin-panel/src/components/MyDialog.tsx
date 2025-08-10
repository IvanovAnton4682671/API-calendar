import { FormSchema, SubmitFunction } from "../types/formSchemas"
import { Dialog, Flex } from "@radix-ui/themes"
import MyFormConstructor from "./MyFormConstructor"
import MyServerZone from "./MyServerZone"
import { useState } from "react"
import { AxiosError } from "axios"
import { ServerResponse } from "./MyServerZone"


function MyDialog({triggerButton, formSchema, submitFunc}:
    {triggerButton: React.ReactNode, formSchema: FormSchema, submitFunc: SubmitFunction}) {
    //состояние ответа сервера
    const [serverResponse, setServerResponse] = useState<ServerResponse | null>(null)

    //обработчик получения ответа сервера
    const handleSubmitSuccess = (response: any) => {
        setServerResponse({ data: response })
    }

    //обработчик получения ошибки от сервера
    const handleSubmitError = (error: AxiosError | any) => {
        setServerResponse({ error: error })
    }

    //состояние сброса ответа сервера при открытии формы
    const [isOpen, setIsOpen] = useState<boolean>(false)
    //состояние сброса формы
    const [formKey, setFormKey] = useState<number>(0)

    //обработчик сброса ответа сервера при открытии формы
    const handleOpenChange = (open: boolean) => {
        setIsOpen(open)
        if (open) {
            setServerResponse(null)
            setFormKey(prev => prev + 1)
        }
    }

    return(
        <Dialog.Root open={isOpen} onOpenChange={handleOpenChange}>
            <Dialog.Trigger>{triggerButton}</Dialog.Trigger>
            {isOpen && (
                <Dialog.Content maxWidth={serverResponse ? "1200px" : "600px"}>
                    <Flex direction="row" gap="5">
                        <Flex direction="column" width={serverResponse ? "50%" : "100%"}>
                            <Dialog.Title size="5" mb="3">{formSchema.title}</Dialog.Title>
                            <Dialog.Description size="3" mb="5">{formSchema.description}</Dialog.Description>
                            <MyFormConstructor
                                key={formKey}
                                formSchema={formSchema}
                                submitFunc={submitFunc}
                                onSubmitSuccess={handleSubmitSuccess}
                                onSubmitError={handleSubmitError}
                            />
                        </Flex>
                        {serverResponse && (
                            <MyServerZone serverResponse={serverResponse} />
                        )}
                    </Flex>
                </Dialog.Content>
            )}
        </Dialog.Root>
    )
}

export default MyDialog