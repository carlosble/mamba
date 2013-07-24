from mamba import describe, context, before
from sure import expect
from doublex import *

from mamba import reporters, formatters, spec

ANY_SPEC = spec.Spec(None)
ANY_SPEC_GROUP = spec.SpecGroup(None)


with describe(reporters.Reporter) as _:

    @before.each
    def create_reporter_and_attach_formatter():
        _.formatter = Spy(formatters.Formatter)
        _.reporter = reporters.Reporter(_.formatter)

    def it_notifies_event_spec_started_to_listeners():
        _.reporter.spec_started(ANY_SPEC)

        assert_that(_.formatter.spec_started, called().with_args(ANY_SPEC))

    def it_increases_spec_counter_when_spec_started():
        _.reporter.spec_started(ANY_SPEC)

        expect(_.reporter.spec_count).to.be.equal(1)

    def it_notifies_event_spec_passed_to_listeners():
        _.reporter.spec_passed(ANY_SPEC)

        assert_that(_.formatter.spec_passed, called().with_args(ANY_SPEC))

    def it_notifies_event_spec_failed_to_listeners():
        _.reporter.spec_failed(ANY_SPEC)

        assert_that(_.formatter.spec_failed, called().with_args(ANY_SPEC))

    def it_increases_failed_counter_when_spec_started():
        _.reporter.spec_failed(ANY_SPEC)

        expect(_.reporter.failed_count).to.be.equal(1)

    def it_notifies_event_spec_pending_to_listeners():
        _.reporter.spec_pending(ANY_SPEC)

        assert_that(_.formatter.spec_pending, called().with_args(ANY_SPEC))

    def it_increases_pending_counter_when_spec_started():
        _.reporter.spec_pending(ANY_SPEC)

        expect(_.reporter.pending_count).to.be.equal(1)

    def it_notifies_event_spec_group_started_to_listeners():
        _.reporter.spec_group_started(ANY_SPEC_GROUP)

        assert_that(_.formatter.spec_group_started, called().with_args(ANY_SPEC_GROUP))

    def it_notifies_event_spec_group_finished_to_listeners():
        _.reporter.spec_group_finished(ANY_SPEC_GROUP)

        assert_that(_.formatter.spec_group_finished, called().with_args(ANY_SPEC_GROUP))

    with context('when finishing'):
        def it_notifies_summary_to_listeners():
            _.reporter.finish()

            assert_that(_.formatter.summary, called().with_args(_.reporter.spec_count, _.reporter.failed_count, _.reporter.pending_count))