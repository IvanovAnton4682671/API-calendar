import { mySize } from "../../types/radixElems"
import { Text, Flex, Switch } from "@radix-ui/themes"

function MySwitchField({dataReceiver, onCheckedChange, field, leftText, rightText, size, name}:
    {dataReceiver: any, onCheckedChange: (data: any) => void, field: any, leftText: string, rightText: string, size: mySize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <Flex align="center" gap="2">
                <Text size={size}>{leftText}</Text>
                <Switch
                    name={name}
                    id={name}
                    checked={dataReceiver}
                    onCheckedChange={onCheckedChange}
                />
                <Text size={size}>{rightText}</Text>
            </Flex>
        </label>
    )
}

export default MySwitchField