import React from "react";
import moment from "moment";
import * as Chakra from "@chakra-ui/react";
import { TimeIcon } from "@chakra-ui/icons";

const Match = ({
  datetime,
  stadium,
  type,
  seats,
  booked_seats,
  COUNTRY1,
  COUNTRY2,
}) => {
  let date = new Date(datetime);
  let formattedDate = moment(date).format("DD-MM-YYYY");
  let formattedTime = moment(date).format("h:mm A");

  let badgeColorScheme = {
    t20: "blue.500",
    odi: "green.500",
    test: "orange.500",
  };

  let btn_msg = "Book Now!";
  let seatsBooked = false;
  let matchBeingPlayed = false;

  if (date.getTime() < Date.now()) {
    btn_msg = "Match Is Going On";
    matchBeingPlayed = true;
  } else if (seats - booked_seats === 0) {
    btn_msg = "Seats Already Booked";
    seatsBooked = true;
  }

  return (
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
          <Chakra.Heading size="md">
            <span style={{ textTransform: "capitalize" }}>{stadium}</span>
          </Chakra.Heading>
          <Chakra.Text
            fontWeight={"bold"}
            color={"black"}
            borderRadius="md"
            px={1}
            background={badgeColorScheme[type]}
            casing="uppercase"
          >
            {type}
          </Chakra.Text>
        </Chakra.Flex>
        <Chakra.Box
          borderRadius="full"
          h={1}
          w="100%"
          my={3}
          bg="whiteAlpha.700"
        />

        <Chakra.Flex
          w="100%"
          justifyContent={"space-evenly"}
          py={2}
          mb={2}
          borderRadius="lg"
          bg={"whiteAlpha.200"}
        >
          <Chakra.Heading size="sm">
            <span style={{ textTransform: "capitalize" }}>{COUNTRY1}</span>
          </Chakra.Heading>
          <Chakra.Text size="sm">vs</Chakra.Text>
          <Chakra.Heading size="sm">
            <span style={{ textTransform: "capitalize" }}>{COUNTRY2}</span>
          </Chakra.Heading>
        </Chakra.Flex>

        <Chakra.Flex alignItems="center" justifyContent={"space-between"}>
          <Chakra.Flex fontWeight={"thin"} alignItems="center">
            <TimeIcon mr={2} />
            <span>
              <Chakra.Text>{formattedDate}</Chakra.Text>
              <Chakra.Text>{formattedTime}</Chakra.Text>
            </span>
          </Chakra.Flex>

          <Chakra.Button
            size={"sm"}
            flexGrow={1}
            ml={5}
            colorScheme={
              matchBeingPlayed ? "red" : seatsBooked ? "yellow" : "blue"
            }
            isDisabled={seatsBooked || matchBeingPlayed}
          >
            {btn_msg}
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
            Remaining Seats: {(booked_seats / seats) * 100}
          </Chakra.Text>
          <Chakra.Box
            borderRadius="full"
            h={0.5}
            flexGrow={1}
            bg="whiteAlpha.300"
          />
        </Chakra.Flex>

        <Chakra.Progress
          height={2}
          borderRadius={"full"}
          value={(booked_seats / seats) * 100}
        />
      </Chakra.CardBody>
    </Chakra.Card>
  );
};

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
          <Match
            stadium="Chinna Swami Stgadium"
            datetime="2023-03-01 13:59:52"
            type="t20"
            seats={500}
            booked_seats={500}
            COUNTRY1="USA"
            COUNTRY2="AUS"
          />
          <Match
            stadium="Aussies Flare Stadium"
            datetime="2023-02-01 11:59:52"
            type="odi"
            seats={500}
            booked_seats={200}
            COUNTRY1="USA"
            COUNTRY2="AUS"
          />
          <Match
            stadium="Great Eagle Stadium"
            datetime="2023-12-01 19:59:42"
            type="test"
            seats={500}
            booked_seats={300}
            COUNTRY1="USA"
            COUNTRY2="AUS"
          />
        </Chakra.Flex>
      </Chakra.Container>
    </Chakra.Box>
  );
};

export default Matches;
