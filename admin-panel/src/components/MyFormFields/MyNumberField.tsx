import type { ThemeConfig } from "antd";
import { theme as antdTheme, ConfigProvider, InputNumber } from "antd";
import { mySize } from "../../types/radixElems";
import { Text } from "@radix-ui/themes";

//тёмная тема типа как в Radix
const darkTheme: ThemeConfig = {
    algorithm: antdTheme.darkAlgorithm,
    token: {
        colorPrimary: '#4a4e4c',
        colorBgContainer: '#111312',
        colorText: '#fafafa',
        colorTextPlaceholder: '#5c5c5e',
        colorIcon: '#5c5c5e',
        colorBorder: '#4a4e4c',
        borderRadius: 6,
    },
    components: {
        InputNumber: {
            activeBorderColor: '#277f70',
            activeShadow: '0 0 0 2px rgba(134, 239, 172, 0.1)',
            paddingBlock: 8,
            paddingInline: 12,
        },
    },
}

function MyNumberField({dataReceiver, onChange, field, size, name}:
    {dataReceiver: any, onChange: (data: any) => void, field: any, size: mySize, name: string}) {
    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold">{field.label}</Text>
            <ConfigProvider theme={darkTheme}>
                <InputNumber
                    name={name}
                    id={name}
                    value={dataReceiver}
                    onChange={onChange}
                />
            </ConfigProvider>
        </label>
    )
}

export default MyNumberField