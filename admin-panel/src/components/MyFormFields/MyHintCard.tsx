import { HoverCard, Link, ScrollArea, Flex, Text } from "@radix-ui/themes"

function MyHintCard({link, fieldHint}: {link: string, fieldHint: string}) {
    return(
        <HoverCard.Root>
            <HoverCard.Trigger>
                <Link>{link}</Link>
            </HoverCard.Trigger>
            <HoverCard.Content side="bottom" align="center" maxWidth="700px">
                <ScrollArea type="auto" scrollbars="vertical" style={{maxHeight: "400px"}}>
                    <Flex style={{paddingRight: "25px"}}>
                        <Text style={{whiteSpace: "pre-line"}}>{fieldHint}</Text>
                    </Flex>
                </ScrollArea>
            </HoverCard.Content>
        </HoverCard.Root>
    )
}

export default MyHintCard