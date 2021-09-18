# NucleusID

Your online identity. This project is a WIP.

## Running

You can run this app with Docker!

Copy `.env.example` to `.env`, fill in the configurations, and run the following command.

```sh
docker-compose up
```

Now, simply access http://localhost:5000 to use the app!

Note:
- Some configurations cannot be changed and are specified in `config/docker.env`.
- When you change certain configurations, you need to rebuild the client files.

## Running (development)

Here are the steps for running this project in development.

### Prerequisites

- Node.js 16+
- Python 3.9+
- Rust 1.55+
- PostgreSQL
- Redis

### Dependencies

To install the dependencies, run the following commands.

```sh
cargo install diesel_cli
npm install -g yarn
pip3 install -U poetry
yarn
poetry install
```

### Configuration

Copy `.example.env` to `.env` and fill in the configurations.

Then, set up the database with the following command
```sh
./scripts/database.sh setup
```

### Running

Finally, run the project with these commands in two terminals.

```sh
yarn dev
poetry run poe dev
```

Now go to the specified address!

## License

This project is licensed under the [MIT License](LICENSE).
