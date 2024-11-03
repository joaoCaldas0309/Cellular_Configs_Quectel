commands = [b"TESTE", b"TESTE", b"TESTE", b"TESTE"]
    responses = []
    with tqdm(total=len(commands), desc="Configuring Argentina APN", leave=True, ncols=80) as progress_bar:
        for command in commands:
            ser.write(command)
            if ser.in_waiting:
                response = ser.readline().decode().strip()
                responses.append(response)
            time.sleep(1)
            progress_bar.update(1)
    tqdm.write("\nDevices response: ", + str(responses))