import { myTextAreaSize } from "../../types/radixElems"
import { Text, Select } from "@radix-ui/themes"

function MySelectField({dataReceiver, onValueChange, field, size, name}:
    {dataReceiver: any, onValueChange: (data: any) => void, field: any, size: myTextAreaSize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <Select.Root
                name={name}
                size={size}
                value={dataReceiver}
                onValueChange={onValueChange}
            >
                <Select.Trigger />
                <Select.Content>
                    <Select.Group>
                        <Select.Label>{field.label}</Select.Label>
                        {Object.entries(field.options).map(([value, label]) => (
                            <Select.Item key={value} value={value}>{label as string}</Select.Item>
                        ))}
                    </Select.Group>
                </Select.Content>
            </Select.Root>
        </label>
    )
}

export default MySelectField