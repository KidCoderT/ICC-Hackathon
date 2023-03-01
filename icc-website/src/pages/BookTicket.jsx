import React from "react";
import * as Chakra from "@chakra-ui/react";
import { ViewIcon } from "@chakra-ui/icons";

const PasswordInput = ({ value, onChange }) => {
  const [show, setShow] = React.useState(false);
  const handleClick = () => setShow(!show);

  return (
    <Chakra.InputGroup size="md" px={3} mb={3}>
      <Chakra.Input
        value={value}
        onChange={onChange}
        pr="4.5rem"
        type={show ? "text" : "password"}
        placeholder="Enter password"
      />
      <Chakra.InputRightElement width="4.5rem">
        <Chakra.IconButton
          icon={<ViewIcon />}
          h="1.75rem"
          size="sm"
          variant={"unstyled"}
          onClick={handleClick}
        />
      </Chakra.InputRightElement>
    </Chakra.InputGroup>
  );
};

const BookTicket = () => {
  const [userMade, setUserMade] = React.useState(false);
  const [fname, setFName] = React.useState("");
  const [lname, setLName] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [redoPassword, setRedoPassword] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [dob, setDob] = React.useState("");
  const [nationality, setNationality] = React.useState("");
  const [gender, setGender] = React.useState("");

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
        {userMade ? (
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

            <Chakra.Flex mb={3} px={3}>
              {/* F Name */}
              <Chakra.Input
                value={fname}
                onChange={setFName}
                textAlign="center"
                placeholder="First Name"
                variant="outline"
                mr={3}
              />

              {/* L Name */}
              <Chakra.Input
                value={lname}
                onChange={setLName}
                textAlign="center"
                placeholder="Last Name"
                variant="outline"
              />

              {/* Email */}
              <Chakra.Input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                textAlign="center"
                placeholder="Email"
                variant="outline"
              />
            </Chakra.Flex>
            {/* Password - Hashed */}
            <PasswordInput value={password} onChange={setPassword} />

            <Chakra.Button colorScheme="green" w="100%" mt={6}>
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

            <Chakra.Flex mb={3} px={3}>
              {/* F Name */}
              <Chakra.Input
                value={fname}
                onChange={setFName}
                textAlign="center"
                placeholder="First Name"
                variant="outline"
                mr={3}
              />

              {/* L Name */}
              <Chakra.Input
                value={lname}
                onChange={setLName}
                textAlign="center"
                placeholder="Last Name"
                variant="outline"
              />

              {/* Email */}
              <Chakra.Input
                value={email}
                onChange={setEmail}
                textAlign="center"
                placeholder="Email"
                variant="outline"
              />
            </Chakra.Flex>

            {/* Date of Birth */}
            <Chakra.Flex direction="column" mb={3} px={3}>
              <label>Date of Birth</label>
              <Chakra.Input
                type="date"
                value={dob}
                onChange={setDob}
                textAlign="center"
                placeholder="Date of Birth"
                variant="outline"
              />
            </Chakra.Flex>

            {/* Nationality */}
            <Chakra.Flex mb={3} px={3} flexDirection="column">
              <Chakra.FormLabel>Nationality</Chakra.FormLabel>
              <Chakra.Select
                value={nationality}
                onChange={setNationality}
                textAlign="center"
                placeholder="Select your nationality"
                variant="outline"
              >
                <option value="AUS">AUS</option>
                <option value="IND">IND</option>
                <option value="AFR">AFR</option>
                <option value="UK">UK</option>
                <option value="BAN">BAN</option>
              </Chakra.Select>
            </Chakra.Flex>

            {/* Gender */}
            <Chakra.Flex direction="column" mb={3} px={3}>
              <label>Gender</label>
              <Chakra.Select
                placeholder="Select Gender"
                value={gender}
                onChange={setGender}
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </Chakra.Select>
            </Chakra.Flex>

            {/* Image Path*/}
            {/* <Chakra.Input
              value={imagePath}
              onChange={setImagePath}
              textAlign="center"
              placeholder="Image Path"
              variant="outline"
              mt={3}
            /> */}

            {/* Password - Hashed */}
            <PasswordInput value={password} onChange={setPassword} />
            <PasswordInput value={redoPassword} onChange={setRedoPassword} />

            <Chakra.Button colorScheme="green" w="100%" mt={6}>
              Send Verification
            </Chakra.Button>
          </>
        )}
      </Chakra.Box>
    </Chakra.Flex>
  );
};

export default BookTicket;
