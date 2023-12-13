import React, { Component} from 'react';

import {
    Box,
    Heading,
    Grommet,
    Table,
    TableBody,
    TableCell,
    TableRow
} from 'grommet';

import './App.css';

const theme = {
    global: {
        colors: {
            brand: '#1a4db4',
            focus: '#1a4db4'
        },
        font: {
            family: 'Lato',
        },
    },
};

export class ViewOneHistory extends Component {
    state = { medhiststate: [], medhiststate2: []}
    componentDidMount() {
        const { email } = this.props.match.params;
        this.getHistory(email);
    }

    getHistory(value) {
        // let email = "'" + value + "'";
        fetch('http://localhost:3001/OneHistory?patientEmail='+ value)
        .then(res => res.json())
            .then(res => {
                this.allDiagnoses(value);
                this.setState({ medhiststate: res.data })
            });
    }

    allDiagnoses(value) {
        // let email = "'" + value + "'";
        fetch('http://localhost:3001/allDiagnoses?patientEmail='+ value)
        .then(res => res.json())
        .then(res => this.setState({ medhiststate2: res.data }));
    }

    render() {
        const { medhiststate } = this.state;
        const { medhiststate2 } = this.state;
        const Header = () => (
            <Box
                tag='header'
                background='brand'
                pad='small'
                elevation='small'
                justify='between'
                direction='row'
                align='center'
                flex={false}
            >
                <a style={{ color: 'inherit', textDecoration: 'inherit'}} href="/"><Heading level='3' margin='none'>HMS</Heading></a>
            </Box>
        );
        const Body = () => (
            <div className="container">
                <div className="panel panel-default p50 uth-panel">
                    {medhiststate.map(patient =>
                        <Table>
                            <TableBody>
                                <TableRow>
                                    <TableCell scope="row">
                                        <strong>Name</strong>
                                    </TableCell>
                                    <TableCell>{patient[1]}</TableCell>
                                    <TableCell></TableCell>
                                    <TableCell><strong>Email</strong></TableCell>
                                    <TableCell>{patient[2]}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                        <strong>Gender</strong>
                                    </TableCell>
                                    <TableCell>
                                        {patient[0]}
                                    </TableCell>
                                    <TableCell />
                                    <TableCell>
                                        <strong>Address</strong>
                                    </TableCell>
                                    <TableCell>{patient[3]}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <strong>Conditions</strong>
                                    </TableCell>
                                    <TableCell>{patient[4]}
                                        </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <strong>Surgeries</strong>
                                    </TableCell>
                                    <TableCell>{patient[5]}
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <strong>Medications</strong>
                                    </TableCell>
                                    <TableCell>{patient[6]}
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    )}
                </div>
                <hr />
            </div>
        );
        const Body2 = () => (
            <div className="container">
                <div className="panel panel-default p50 uth-panel">
                    {medhiststate2.map(patient =>
                        <div>
                        <Table>
                            <TableBody>
                                <TableRow>
                                    <TableCell><strong>Doctor</strong></TableCell>
                                    <TableCell>{patient[1]}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                        <strong>Concerns</strong>
                                    </TableCell>
                                    <TableCell>
                                        {patient[2]}
                                    </TableCell>
                                    <TableCell />
                                    <TableCell>
                                        <strong>Symptoms</strong>
                                    </TableCell>
                                    <TableCell>{patient[3]}</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <strong>Diagnosis</strong>
                                    </TableCell>
                                    <TableCell>{patient[4]}
                                        </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <strong>Prescription</strong>
                                    </TableCell>
                                    <TableCell>{patient[5]}
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell scope="row">
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                        <hr />
                        </div>
                    )}
                </div>
            </div>
        );
        return (
            <Grommet full={true} theme={theme}>
                <Box fill={true}>
                    <Header />
                    <Body />
                    <Body2 />
                </Box>
            </Grommet>
        );
    }
}
export default ViewOneHistory;