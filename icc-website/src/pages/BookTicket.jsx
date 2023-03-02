import React from "react";
import * as Chakra from "@chakra-ui/react";
import { ChevronDownIcon, ViewIcon } from "@chakra-ui/icons";
import { useSearchParams } from "react-router-dom";

const PasswordInput = ({ value, onChange }) => {
  const [show, setShow] = React.useState(false);
  const handleClick = () => setShow(!show);

  return (
    <Chakra.InputGroup size="md" px={3} mb={1}>
      <Chakra.Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
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
  const [params, _] = useSearchParams()

  const [userMade, setUserMade] = React.useState(true);
  const [fname, setFName] = React.useState("");
  const [lname, setLName] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [phone, setPhone] = React.useState("");
  const [dob, setDob] = React.useState("");
  const [nationality, setNationality] = React.useState("");
  const [gender, setGender] = React.useState("");
  const [selectedImage, setSelectedImage] = React.useState(null);
  
  const loginAndCreateTicket = () => {
    if (fname.length === 0 || lname.length === 0) {
      return
    }

    if (password.length === 0) {
      return
    }

    fetch(
      'https://localhost:8080/ticket/create/', {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "info": JSON.parse(params.get("info")),
          "user": {
            "first_name": fname,
            "last_name": lname,
            "password": password
          }
        })
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  const SingupAndMakeTicket = () => {
    if (fname.length === 0 || lname.length === 0) {
      return
    }

    if (password.length === 0) {
      return
    }

    let user = {
      gender: gender,
      nationality: nationality,
      first_name: fname,
      last_name: lname,
      dob: dob,
      email: email,
      phone: phone,
      password: password,
    }; 

    const formDataJson = JSON.stringify(user);

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      body: formDataJson,
    };

    const fileData = new FormData();
    fileData.append('image_file', selectedImage);
    fileData.append('json_info', formDataJson);

    requestOptions.body = fileData;

    fetch('https://localhost:8080/person/create/' + formDataJson, requestOptions).then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.error(error);
    });;
    
  }

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
                onChange={(e) => setFName(e.target.value)}
                textAlign="center"
                placeholder="First Name"
                variant="outline"
                mr={3}
              />

              {/* L Name */}
              <Chakra.Input
                value={lname}
                onChange={(e) => setLName(e.target.value)}
                textAlign="center"
                placeholder="Last Name"
                variant="outline"
              />
            </Chakra.Flex>
            {/* Password - Hashed */}
            <PasswordInput value={password} onChange={setPassword} />
            
            <Chakra.Button w="100%" variant="link" mt={6} onClick={() => {setUserMade(false)}}>
              Dont have. Account? Create One
            </Chakra.Button>

            <Chakra.Button colorScheme="green" w="100%" mt={6} onClick={loginAndCreateTicket}>
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
                onChange={(e) => setFName(e.target.value)}
                textAlign="center"
                placeholder="First Name"
                variant="outline"
                mr={3}
              />

              {/* L Name */}
              <Chakra.Input
                value={lname}
                onChange={(e) => setLName(e.target.value)}
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

            <Chakra.Input
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                textAlign="center"
                placeholder="Phone Number"
                variant="outline"
              />

            {/* Date of Birth */}
            <Chakra.Flex direction="column" mb={3} px={3}>
              <label>Date of Birth</label>
              <Chakra.Input
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                textAlign="center"
                placeholder="Date of Birth"
                variant="outline"
              />
            </Chakra.Flex>

            {/* Nationality */}
            <Chakra.Flex mb={3} px={3} flexDirection="column">
              <Chakra.Menu>
                <Chakra.MenuButton
                  flexGrow={1}
                  as={Chakra.Button}
                  rightIcon={<ChevronDownIcon />}
                  colorScheme="whiteAlpha"
                  variant="outline"
                >
                  {nationality || "Whats your Nationality..."}
                </Chakra.MenuButton>

                <Chakra.MenuList colorScheme="whiteAlpha" variant="outline">
                  {["AUS", "IND", "AFR", "UK", "BAN"].map((item, key) => (
                    <Chakra.MenuItem
                      key={key}
                      color="black"
                      onClick={() => {
                        setNationality(item);
                      }}
                    >
                      {item}
                    </Chakra.MenuItem>
                  ))}
                </Chakra.MenuList>
              </Chakra.Menu>
            </Chakra.Flex>

            {/* Gender */}
            <Chakra.Flex direction="column" mb={3} px={3}>
              <Chakra.Menu>
                <Chakra.MenuButton
                  flexGrow={1}
                  as={Chakra.Button}
                  rightIcon={<ChevronDownIcon />}
                  colorScheme="whiteAlpha"
                  variant="outline"
                >
                  {gender || "Gender"}
                </Chakra.MenuButton>

                <Chakra.MenuList colorScheme="whiteAlpha" variant="outline">
                  {["male", "female", "other"].map((item, key) => (
                    <Chakra.MenuItem
                      key={key}
                      color="black"
                      onClick={() => {
                        setGender(item);
                      }}
                    >
                      {item}
                    </Chakra.MenuItem>
                  ))}
                </Chakra.MenuList>
              </Chakra.Menu>
            </Chakra.Flex>

            <Chakra.Flex direction="column" mb={3} px={3}>
              <Chakra.FormLabel htmlFor="image-upload" textAlign="center">
                Upload Image
              </Chakra.FormLabel>
              <input
        type="file"
        name="myImage"
        onChange={(event) => {
          setSelectedImage(event.target.files[0]);
        }}
      />
            </Chakra.Flex>

            {/* Password - Hashed */}
            <PasswordInput value={password} onChange={setPassword} />

            <Chakra.Button w="100%" variant="link" mt={6} onClick={() => {setUserMade(true)}}>
              Already have Account? Sign In
            </Chakra.Button>

            <Chakra.Button colorScheme="green" w="100%"  onClick={SingupAndMakeTicket} mt={6}>
              Send Verification
            </Chakra.Button>
          </>
        )}
      </Chakra.Box>
    </Chakra.Flex>
  );
};

export default BookTicket;
