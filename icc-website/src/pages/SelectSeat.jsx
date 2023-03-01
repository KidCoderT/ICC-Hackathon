import React from "react";
import * as Chakra from "@chakra-ui/react";
import { ChevronDownIcon, ViewIcon } from "@chakra-ui/icons";

blocks = [
  { label: "", rows: [{ name: "", seats: [true, false] }] },
  { label: "", rows: [{ name: "", seats: [true, false] }] },
  { label: "", rows: [{ name: "", seats: [true, false] }] },
  { label: "", rows: [{ name: "", seats: [true, false] }] },
  { label: "", rows: [{ name: "", seats: [true, false] }] },
  { label: "", rows: [{ name: "", seats: [true, false] }] },
];

const SelectSeat = () => {
  const { isOpen, onOpen, onClose } = Chakra.useDisclosure();

  return (
    <>
      <Chakra.Modal onClose={onClose} size={"full"} isOpen={isOpen}>
        <Chakra.ModalOverlay />
        <Chakra.ModalContent>
          <Chakra.ModalHeader>Seat Viewing</Chakra.ModalHeader>
          <Chakra.ModalCloseButton />
          <Chakra.ModalBody background={"black"}>
            {/* Seat Viewing */}
          </Chakra.ModalBody>
          <Chakra.ModalFooter textAlign={"center"}>
            <Chakra.Heading size={"md"}>Block: AA, Seat: NAN</Chakra.Heading>
          </Chakra.ModalFooter>
        </Chakra.ModalContent>
      </Chakra.Modal>

      <Chakra.Box as="main" background="blackAlpha.900" minH={"100vh"}>
        <Chakra.Container color="whiteAlpha.800" maxW="80%" py={10}>
          <Chakra.Heading size="2xl" textAlign={"center"}>
            Seat Selection: <div>Chinna Swami Stadium</div>
          </Chakra.Heading>

          <Chakra.Box
            borderRadius="full"
            h={1}
            w="100%"
            my={6}
            bg="whiteAlpha.700"
          />

          <Chakra.Flex
            w="100%"
            justifyContent={"space-evenly"}
            py={2}
            mb={6}
            borderRadius="lg"
            bg={"whiteAlpha.200"}
          >
            <Chakra.Heading size="sm">
              <span style={{ textTransform: "capitalize" }}>AUS</span>
            </Chakra.Heading>
            <Chakra.Text size="sm">vs</Chakra.Text>
            <Chakra.Heading size="sm">
              <span style={{ textTransform: "capitalize" }}>IND</span>
            </Chakra.Heading>
          </Chakra.Flex>

          <Chakra.IconButton
            colorScheme="whiteAlpha"
            variant="outline"
            icon={<ViewIcon />}
            onClick={onOpen}
          />

          {/* Block */}
          <Chakra.Menu>
            <Chakra.MenuButton
              as={Chakra.Button}
              rightIcon={<ChevronDownIcon />}
              colorScheme="whiteAlpha"
              variant="outline"
            >
              Select
            </Chakra.MenuButton>
            <Chakra.MenuList>{}</Chakra.MenuList>
          </Chakra.Menu>

          {/* seats */}

          {/* seat viewing */}
        </Chakra.Container>
      </Chakra.Box>
    </>
  );
};

export default SelectSeat;
