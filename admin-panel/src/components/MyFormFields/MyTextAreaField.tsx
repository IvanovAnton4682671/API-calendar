import { mySize, myTextAreaSize } from "../../types/radixElems"
import { Text, Flex, TextArea } from "@radix-ui/themes"
import MyHintCard from "./MyHintCard"

function MyTextAreaField({dataReceiver, onChange, field, size, areaSize, name}:
    {dataReceiver: any, onChange: (data: any) => void, field: any, size: mySize, areaSize: myTextAreaSize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <Flex align="center" gap="3">
                <TextArea
                    name={name}
                    id={name}
                    value={dataReceiver}
                    onChange={onChange}
                    placeholder={field.placeholder}
                    size={areaSize}
                    style={{width: "100%", height: "400px"}}
                />
                <MyHintCard link="?" fieldHint={field.hint}/>
            </Flex>
        </label>
    )
}

export default MyTextAreaField