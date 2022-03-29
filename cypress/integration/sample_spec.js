describe("테스트 1", () => {
    it("테스트 세부사항 1", () => {
        cy.visit("/")
    })
    it("테스트 세부사항 2", () => {
        cy.visit("/")
        cy.contains("Learn React")
    })
    it("테스트 세부사항 3", () => {
         cy.visit("/")
        cy.contains("Learn React123")
    })
})