import React from "react";
import * as Chakra from "@chakra-ui/react";
import { TimeIcon } from "@chakra-ui/icons";

const Match = () => (
  <Chakra.Card
    boxShadow="lg"
    background="blackAlpha.500"
    color="whiteAlpha.900"
    minW="sm"
    maxW="md"
    flexGrow={1}
    m={2}
  >
    <Chakra.CardBody>
      <Chakra.Flex justifyContent={"space-between"}>
        <Chakra.Heading size="md">China Swami Stadium</Chakra.Heading>
        <Chakra.Text
          fontWeight={"bold"}
          color={"black"}
          borderRadius="md"
          px={1}
          background={"blue.500"}
        >
          T20
        </Chakra.Text>
      </Chakra.Flex>
      <Chakra.Box
        borderRadius="full"
        h={1}
        w="100%"
        my={3}
        bg="whiteAlpha.700"
      />

      <Chakra.Flex alignItems="center" justifyContent={"space-between"}>
        <Chakra.Flex fontWeight={"thin"} alignItems="center">
          <TimeIcon mr={2} />
          <span>
            <Chakra.Text>23-10-2023</Chakra.Text>
            <Chakra.Text>5:20 PM IST</Chakra.Text>
          </span>
        </Chakra.Flex>

        <Chakra.Button size={"sm"} flexGrow={1} ml={5} colorScheme={"yellow"}>
          Book Now!
        </Chakra.Button>
      </Chakra.Flex>

      <Chakra.Flex alignItems={"center"} py={1}>
        <Chakra.Box
          borderRadius="full"
          h={0.5}
          flexGrow={1}
          bg="whiteAlpha.300"
        />
        <Chakra.Text mb={2} mx={3} fontWeight={"medium"} fontSize="sm">
          Remaining Seats: 300
        </Chakra.Text>
        <Chakra.Box
          borderRadius="full"
          h={0.5}
          flexGrow={1}
          bg="whiteAlpha.300"
        />
      </Chakra.Flex>

      <Chakra.Progress height={2} borderRadius={"full"} value={80} />
    </Chakra.CardBody>
  </Chakra.Card>
);

const Matches = () => {
  return (
    <Chakra.Box as="main" background="blackAlpha.900" minH={"100vh"}>
      <Chakra.Container color="whiteAlpha.800" maxW="80%" py={10}>
        <Chakra.Heading size="2xl" textAlign={"center"}>
          ICC Upcomming Matches
        </Chakra.Heading>

        <Chakra.Box
          borderRadius="full"
          h={1}
          w="100%"
          my={6}
          bg="whiteAlpha.700"
        />

        <Chakra.Flex
          flexWrap={"wrap"}
          w="100%"
          alignItems={"center"}
          justifyContent={"center"}
        >
          <Match />
          <Match />
          <Match />
          <Match />
          <Match />
          <Match />
          <Match />
        </Chakra.Flex>
      </Chakra.Container>
    </Chakra.Box>
  );
};

export default Matches;
