import { Button, Card, CardContent, Grid, Typography } from '@material-ui/core';
import React, { Component } from 'react';
import AddReviewForm from './AddReviewForm';

export default class LandlordDisplayPage extends Component {
    constructor(props) {
        super(props)
        // TODO: replace this with component mount / unmount stuff?
        // since it's not dynamically changing
        this.state = {
            firstName: "",
            lastName: "",
            reviews: [],
        }
        this.landlordID = this.props.match.params.id;
        this.getLandlordDetails();
    }

    getLandlordDetails = () => {
        fetch('/api/get-landlord-by-id?id=' + this.landlordID)
            .then((response) => response.json())
            .then((data) => this.setState({
                firstName: data.first_name,
                lastName: data.last_name,
            }));
        fetch('/api/get-reviews-for-landlord?landlordID=' + this.landlordID)
            .then((response) => response.json())
            .then((data) => this.setState({
                reviews: data,
            }));
    }

    render() {
        let renderReviews = this.state.reviews.map(
            (review) => {
                return (
                    <Card>
                        <CardContent>
                            <Typography component='h6' variant="h6">
                                {review.reviewer_name} • {review.overall_rating} Overall
                            </Typography>
                            <Typography color="textSecondary">
                                posted on {review.created_at}
                            </Typography>
                            <Typography component="p">
                                Safety Measures / Inspections Rating: {review.safety_rating}
                                <br />
                                Responsiveness / Timely Maitenance Rating: {review.responsiveness_rating}
                                <br />
                                Transparency / Trustworthiness Rating: {review.transparency_rating}
                                <br />
                                Organization / Cleanliness Rating: {review.organization_rating}
                                <br />
                                Student-friendliness Rating: {review.student_friendliness_rating}
                            </Typography>
                        </CardContent>
                    </Card>
                );
            }
        );
        return (
            <Grid container spacing={2} style={{height: "100%"}}>
                <Grid item xs={12} align="center">
                    <Typography component='h5' variant="h5">
                        Reviews for {this.state.firstName} {this.state.lastName} 
                    </Typography>
                </Grid>
                &emsp;
                <Grid item xs={12} align="center" style={{maxHeight: "40%", overflowY: "scroll"}}>
                   {renderReviews}
                </Grid>
                <Grid item xs={12} align="center" style={{maxHeight: "40%", overflowY: "scroll"}}>
                   <AddReviewForm landlordID={this.landlordID} />
                </Grid>
                &emsp;
                <Grid item xs={12} align="center">
                    <Button size="small" href="/search" component="a">Back to Search</Button>
                </Grid>
            </Grid>
        );
    }
}