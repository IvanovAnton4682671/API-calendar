import { mySize } from "../../types/radixElems";
import { Text } from "@radix-ui/themes"
import { DatePicker, ConfigProvider, theme as antdTheme } from 'antd';
import type { ThemeConfig } from "antd";
import ruRU from "antd/locale/ru_RU";
import type { Dayjs } from 'dayjs';
import dayjs from 'dayjs';
import 'dayjs/locale/ru';
import updateLocale from 'dayjs/plugin/updateLocale';
import { useMemo } from 'react';

//настройка русского календаря
dayjs.locale("ru")
dayjs.extend(updateLocale)
dayjs.updateLocale("ru", {
    months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
    monthsShort: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
    weekdays: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
    weekdaysShort: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]
})

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
        DatePicker: {
            activeBorderColor: '#277f70',
            activeShadow: '0 0 0 2px rgba(134, 239, 172, 0.1)',
            paddingBlock: 8,
            paddingInline: 12,
        },
    },
}

function MyDatePickerField({dataReceiver, onChange, field, size, name}:
    {dataReceiver: any, onChange: (data: any) => void, field: any, size: mySize, name: string}) {

    //обработка даты
    const dateValue = useMemo(() => {
        return dataReceiver ? dayjs(dataReceiver, 'YYYY-MM-DD') : null;
    }, [dataReceiver]);
    const handleDateChange = (date: Dayjs | null) => {
        onChange(date ? date.format('YYYY-MM-DD') : '');
    };

    return(
        <label>
            <Text as="div" size={size} mb="2" weight="bold" >{field.label}</Text>
            <ConfigProvider locale={ruRU} theme={darkTheme}>
                <DatePicker
                    name={name}
                    id={name}
                    value={dateValue}
                    onChange={handleDateChange}
                    format="YYYY-MM-DD"
                    allowClear={false}
                />
            </ConfigProvider>
        </label>
    )
}

export default MyDatePickerField