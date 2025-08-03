import { Flex, Text } from "@radix-ui/themes"
import { MyTable } from "../../consts/myTable"
import MyDialog from "../../components/MyDialog"

function Home() {
    return(
        <Flex height="100vh" align="center" justify="center">
            <Flex gap="3">
                {MyTable.columns.map((column, colIndex) => (
                    <Flex key={colIndex} direction="column" align="center" gap="3">
                        <Text size="4" weight="bold" color={column.color}>{column.title}</Text>
                        <Flex direction="column" align="center" gap="3">
                            {column.items.map((item, itemIndex) => (
                                <MyDialog
                                    key={itemIndex}
                                    triggerButton={item.button}
                                    formSchema={item.data}
                                    submitFunc={item.submitFunc}
                                />
                            ))}
                        </Flex>
                    </Flex>
                ))}
            </Flex>
        </Flex>
    )
}

export default Home