import React from "react";
import * as Chakra from "@chakra-ui/react";

const BookTicket = () => {
  let page = 2;

  return (
    <Chakra.Flex
      alignItems={"center"}
      justifyContent="center"
      as="main"
      color="whiteAlpha.800"
      background="blackAlpha.900"
      minH={"100vh"}
    >
      <Chakra.Box
        minW="400px"
        maxW="600px"
        boxShadow="xs"
        bg="black"
        py={5}
        px={5}
        borderRadius="xl"
      >
        {page === 1 ? (
          <>
            <Chakra.Heading size="lg" textAlign={"center"}>
              Login
            </Chakra.Heading>
            <Chakra.Box
              borderRadius="full"
              h={1}
              w="100%"
              my={6}
              bg="whiteAlpha.700"
            />

            {/* F Name */}
            {/* L Name */}
            {/* Password - Hashed */}

            <Chakra.Button
              colorScheme="green"
              // On click go to login
              w="100%"
              mt={2}
            >
              Send Verification
            </Chakra.Button>
          </>
        ) : (
          <>
            <Chakra.Heading size="lg" textAlign={"center"}>
              Signup
            </Chakra.Heading>
            <Chakra.Box
              borderRadius="full"
              h={1}
              w="100%"
              my={6}
              bg="whiteAlpha.700"
            />
            {/* img_path = sql.Column(sql.String(255))

    gender = sql.Column(sql.Enum(GenderEnum, native_enum=True))
    nationality = sql.Column(sql.String(3))
    first_name = sql.Column(sql.String(50))
    last_name = sql.Column(sql.String(50))
    dob = sql.Column(sql.Date)

    email = sql.Column(sql.String(255))
    phone = sql.Column(sql.String(20))

    password = sql.Column(sql.String(255)) # hashed
    rewrite password */}
            <Chakra.Button
              colorScheme="green"
              // On click go to login
              w="100%"
              mt={2}
            >
              Create Person & Ticket
            </Chakra.Button>
          </>
        )}
      </Chakra.Box>
    </Chakra.Flex>
  );
};

export default BookTicket;
