import { mySize } from "../../types/radixElems"
import { Text, RadioGroup, Flex } from "@radix-ui/themes"

function MyRadioField({dataReceiver, onValueChange, field, size, name}:
    {dataReceiver: any, onValueChange: (data: any) => void, field: any, size: mySize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <RadioGroup.Root
                name={name}
                id={name}
                value={dataReceiver}
                onValueChange={onValueChange}
            >
                <Flex gap="2">
                    {Object.entries(field.options).map(([value, label]) => (
                        <label key={value}>
                            <Flex align="center" gap="2">
                                <RadioGroup.Item value={value}/>
                                <Text size={size}>{label as string}</Text>
                            </Flex>
                        </label>
                    ))}
                </Flex>
            </RadioGroup.Root>
        </label>
    )
}

export default MyRadioField