import { mySize } from "../../types/radixElems"
import { Text, Flex, TextField } from "@radix-ui/themes"
import MyHintCard from "./MyHintCard"

function MyTextField({dataReceiver, onChange, field, size, name}: 
    {dataReceiver: any, onChange: (data: any) => void, field: any, size: mySize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <Flex gap="3">
                <TextField.Root
                    name={name}
                    id={name}
                    value={dataReceiver}
                    onChange={onChange}
                    placeholder={field.placeholder}
                    style={{width: "100%"}}
                />
                <MyHintCard link="?" fieldHint={field.hint}/>
            </Flex>
        </label>
    )
}

export default MyTextField